package main

import (
	"fmt"
	"math"
	"sort"
)

const (
	PLL_MIN     = 80e6
	PLL_MAX     = 110e6
	DAC_MOD_MAX = 6.758e6
	TOL         = 1e-9
)

type Rate struct {
	FS   float64
	DOSR float64
}

type RateKey struct {
	FS, DOSR float64
}

type Solution struct {
	PLLCLKIN float64
	FS       float64
	DOSR     float64
	P, R, J  int
	D        int
	NDAC     int
	MDAC     int
}

func better(a, b Solution) bool {
	if a.NDAC != b.NDAC {
		return a.NDAC > b.NDAC
	}
	return a.MDAC < b.MDAC
}

func solvePLL(pllIn, codecCLK float64, NDAC, MDAC int, r Rate) []Solution {
	var solutions []Solution
	for P := 1; P <= 8; P++ {
		for R := 1; R <= 16; R++ {
			for J := 1; J <= 63; J++ {

				if rj := R * J; rj < 4 || rj > 259 {
					continue
				}

				targetMult := codecCLK * float64(P) / (pllIn * float64(R))
				Df := (targetMult - float64(J)) * 10_000.0
				D := int(math.Round(Df))

				if D < 0 || D > 9999 {
					continue
				}

				mult := float64(J) + float64(D)/10_000.0
				pllCLK := pllIn * float64(R) * mult / float64(P)

				if pllCLK < PLL_MIN || pllCLK > PLL_MAX {
					continue
				}

				if math.Abs(pllCLK-codecCLK) > TOL {
					continue
				}

				solutions = append(solutions, Solution{
					PLLCLKIN: pllIn,
					FS:       r.FS,
					DOSR:     r.DOSR,
					P:        P,
					R:        R,
					J:        J,
					D:        D,
					NDAC:     NDAC,
					MDAC:     MDAC,
				})
			}
		}
	}
	return solutions
}

func updateBest(best map[float64]map[RateKey]Solution, s Solution) {
	if best[s.PLLCLKIN] == nil {
		best[s.PLLCLKIN] = make(map[RateKey]Solution)
	}
	key := RateKey{s.FS, s.DOSR}
	cur, ok := best[s.PLLCLKIN][key]
	if !ok || better(s, cur) {
		best[s.PLLCLKIN][key] = s
	}
}

func main() {
	pllClkins := []float64{
		12_500_000,
		6_250_000,
		5_000_000,
	}

	rates := []Rate{
		{8000, 768},
		{11025, 512},
		{22050, 256},
		{44100, 128},
		{48000, 128},
	}

	best := make(map[float64]map[RateKey]Solution)

	for _, pllIn := range pllClkins {
		for _, r := range rates {

			modCLK := r.FS * r.DOSR
			if modCLK > DAC_MOD_MAX {
				continue
			}

			for NDAC := 1; NDAC <= 128; NDAC++ {
				for MDAC := 1; MDAC <= 128; MDAC++ {

					codecCLK := modCLK * float64(NDAC*MDAC)

					sols := solvePLL(pllIn, codecCLK, NDAC, MDAC, r)
					for _, s := range sols {
						updateBest(best, s)
					}
				}
			}
		}
	}

	// Output
	var pllKeys []float64
	for k := range best {
		pllKeys = append(pllKeys, k)
	}
	sort.Float64s(pllKeys)

	for _, pll := range pllKeys {
		fmt.Printf("\nPLL_CLKIN = %.0f Hz\n", pll)

		var rateKeys []RateKey
		for k := range best[pll] {
			rateKeys = append(rateKeys, k)
		}
		sort.Slice(rateKeys, func(i, j int) bool {
			if rateKeys[i].FS == rateKeys[j].FS {
				return rateKeys[i].DOSR < rateKeys[j].DOSR
			}
			return rateKeys[i].FS < rateKeys[j].FS
		})

		for _, rk := range rateKeys {
			s := best[pll][rk]
			fmt.Printf(
				" %5.0f Hz: p, r, j, d, ndac, mdac, dosr = %d, %d, %d, %d, %d, %d, %.0f\n",
				s.FS, s.P, s.R, s.J, s.D, s.NDAC, s.MDAC, s.DOSR,
			)
		}
	}
}
