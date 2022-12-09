#!/bin/sh
mkdir pretrained_models
cd pretrained_models

# wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1bMTNWkh5LArlaWSc_wa8VKyq2V42T2z0' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1bMTNWkh5LArlaWSc_wa8VKyq2V42T2z0" -O psp_ffhq_encode.pt && rm -rf /tmp/cookies.txt

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1EM87UquaoQmk17Q8d5kYIAHqu0dkYqdT' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1EM87UquaoQmk17Q8d5kYIAHqu0dkYqdT" -O stylegan2-ffhq-config-f.pt && rm -rf /tmp/cookies.txt
