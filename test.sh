exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>test.log 2>&1

run_py=`/opt/miniconda/envs/asr/bin/python`

echo "Test 10 minute file:"
ans=(`$run_py model.py test10p.wav`)
echo $ans

echo "Test 500 files:"
mkdir "500test"
arg=""
for i in {1..500}
do
  name=500test/test10p_$i.wav
  cp test10p.wav $name
  $arg=$arg+$name
done
ans=(`$run_py model.py $arg`)
echo $ans