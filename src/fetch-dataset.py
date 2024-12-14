import wget

url = 'https://dano.hse.ru/mirror/pubs/share/987939206.csv'
filepath = '../datasets/ds_raw.csv'

wget.download(url, filepath)
