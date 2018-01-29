#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <errno.h>

static const char* NAMES[] = {
	"Pickles",
	"Bananas",
	"Kimchi",
	"Potatoes",
	"Banana peppers",
	"Chilis"
};

static const char* FOODS[] = {
	"Bob",
	"Tim",
	"Mary",
	"Sue",
	"Jane",
	"Arthur",
	"Zaphod"
};

__attribute__((noinline)) const char* get_name(long idx) {
	if (idx > 5 || idx < 0) {
		return NULL;
	}
	return NAMES[idx];
}

__attribute__((noinline)) const char* get_food(long idx) {
	if (idx > 6 || idx < 0) {
		return NULL;
	}
	return FOODS[idx];
}

int main(int argc, char* argv[]) {
	if (argc < 3) {
		printf("You need to select a type and an index!\n");
		exit(1);
	}
	long idx = strtol(argv[2], NULL, 10);
	if (errno == EINVAL || errno == ERANGE) {
		printf("bad number as second arg: %s\n", argv[2]);
		exit(1);
	}
	char* get_from = argv[1];
	if (strncmp(get_from, "foods", 5) == 0)  {
		const char* food = get_food(idx);
		if (food == NULL) {
			printf("Aw that food doesn't exist :(\n");
			exit(1);
		}
		printf("I don't think the recipe calls for a %s...\n", food);
	} else if (strncmp(get_from, "names", 5) == 0) {
		const char* name = get_name(idx);
		if (name == NULL) {
			printf("Aw that name doesn't exist :(\n");
			exit(1);
		}
		printf("What kind of name is %s?\n", name);
	} else {
		printf("We don't know anything about %s here\n", get_from);
		exit(1);
	}
}
