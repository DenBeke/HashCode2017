#!/bin/sh

echo "Running: me_at_the_zoo"
python main.py < "input/me_at_the_zoo.in" > "output/me_at_the_zoo.out"

echo "Running: kittens"
python main.py < "input/kittens.in" > "output/kittens.out"

echo "Running: trending_today"
python main.py < "input/trending_today.in" > "output/trending_today.out"

echo "Running: videos_worth_spreading"
python main.py < "input/videos_worth_spreading.in" > "output/videos_worth_spreading.out"