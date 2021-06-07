#!/bin/bash
th=2

dir=.
header=$dir/head.star
imgName=`grep '^_rlnImageName' $header | awk '{print substr($2,2)}'`

cp $header $dir/pre_vote.star
cp $header $dir/post_and.star

grep -h mrcs $dir/u*b*c*star | awk '{print $'$imgName'}' | sort | uniq -c > $dir/pre_vote.log
grep -h mrcs $dir/u*b*c*star | sort -k $imgName,$imgName -u >> $dir/pre_vote.star
awk '{if ($1>='$th') {print " "$2}}' $dir/pre_vote.log > $dir/post_vote.log
grep -Ff $dir/post_vote.log $dir/pre_vote.star >> $dir/post_and.star

echo "Particle number before voting:" `grep mrcs pre_vote.star|wc -l`
echo "Particle number after voting:" `grep mrcs post_and.star|wc -l`

