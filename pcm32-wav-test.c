/*
 * pcm32-wav-test.c
 * Vedant Kumar <vsk@berkeley.edu>
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

#include <sndfile.h>

#define DURATION 	3 	/* Length, in seconds. */
#define SAMPLE_RATE 	44100 	/* Samples per second. */
#define VOLUME 		0.5 	/* [0.0, 1.0]. */

#define M_PI 		acos(-1)

/* Generate a value in [-1.0, 1.0]. */ 
typedef float (*snd_generator)(void* state, int frame);

void create_file(const char* name, snd_generator sampler, void* state) {
	SF_INFO sfinfo;
	memset(&sfinfo, 0, sizeof(sfinfo));
	sfinfo.channels = 1;
	sfinfo.samplerate = SAMPLE_RATE;
	int nr_frames = DURATION * SAMPLE_RATE;
	sfinfo.frames = nr_frames;
	sfinfo.format = (SF_FORMAT_WAV | SF_FORMAT_PCM_32);
	SNDFILE* file = sf_open(name, SFM_WRITE, &sfinfo);
	if (!file) {
		puts("Error: couldn't open file for writing.");
		return;
	}

	int* buf = malloc(sizeof(int) * nr_frames);
	if (!buf) {
		puts("Error: couldn't allocate memory for PCM buffer.");
		sf_close(file);
		return;
	}

	int bits = 32;
	/* This logic only works if bits > 8. */
	int64_t range_max = (1LL << bits) - 1;
	int64_t range_diff = (1LL << (bits - 1));
	for (int i=0; i < nr_frames; ++i) {
		/* Clamp the sampler. */
		float val = sampler(state, i) * VOLUME;
		if (val > 1.0) {
			val = 1.0;
		} else if (val < -1.0) {
			val = -1.0;
		}
		/* [-1, 1] -> [0, 1] -> [-2^b-1, 2^b-1] */
		val = (val + 1) / 2; 
		buf[i] = (val * range_max) - range_diff;
	}

	if (sf_write_int(file, buf, nr_frames) != nr_frames) {
		puts("Error: couldn't write the PCM buffer correctly.");
	}
	sf_close(file);
}

/* Create a sine wave. */
struct snd_gen_wave {
	float freq; 	/* Oscillations per second. */
};

static float sine_sampler(void* state, int frame) {
	struct snd_gen_wave* info = state;
	return sin(2 * M_PI * frame * (SAMPLE_RATE / info->freq));
}

/* Combine two generators. */
struct snd_gen_combined {
	void* lhs_state;
	void* rhs_state;
	snd_generator lhs;
	snd_generator rhs;
};

static float combined_sampler(void* state, int frame) {
	struct snd_gen_combined* info = state;
	return (info->lhs(info->lhs_state, frame) +
		info->rhs(info->rhs_state, frame)) / 2;
}
	
int main() {
	struct snd_gen_wave wave1 = {440}; /* A4 */
	create_file("sine-440.wav", sine_sampler, &wave1);

	struct snd_gen_wave wave2 = {523}; /* C5 */
	struct snd_gen_combined wave3 = {&wave1, &wave2, sine_sampler, sine_sampler};
	create_file("combined.wav", combined_sampler, &wave3);

	struct snd_gen_wave wave4 = {699}; /* F5 */
	struct snd_gen_combined wave5 = {&wave3, &wave4, combined_sampler, sine_sampler};
	create_file("combined_combined.wav", combined_sampler, &wave5);

	struct snd_gen_wave wave6 = {350}; /* F4 */
	struct snd_gen_combined wave7 = {&wave1, &wave6, sine_sampler, sine_sampler};
	create_file("beejs_combination.wav", combined_sampler, &wave7);

	create_file("sine-350.wav", sine_sampler, &wave6);

	return 0;
}

