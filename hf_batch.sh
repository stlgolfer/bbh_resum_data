for i in {1..20}
do
    screen -dmS bbh$i python hf_runner.py --prefix=hf_$i
done