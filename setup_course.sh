# repair dependencies via conda

conda install -f netcdf4 -y
conda install -f libpng -y
conda install -f matplotlib -y
# install wradlib from bleeding edge
mkdir tmp
cd tmp
wget --no-check-certificate http://bitbucket.org/wradlib/wradlib/get/default.zip
unzip default.zip
cd wradlib-wradlib*
python setup.py install
cd ~
rm -r tmp
