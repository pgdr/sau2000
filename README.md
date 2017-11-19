# Sau 2000 - The industrial Sheep app

The industrial Sheep app has finally arrived.


```
git clone https://github.com/pgdr/sau2000.git
virtualenv env
source env/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py test
./manage.py runserver
# open http://127.0.0.1:8000/sau/

```


## Future goals

1. The first rule of Sau is that Sau is all there is
2. Registered by ear mark number and name
3. Ability to add new Sau, remove Sau that go out of production
4. Create production year
5. For every year, one must be able to add at least 4 rams and for ewes per Sau
6. For each of these lambs, add
  a. ear mark unmber
  b. quality (e, u, r, o, p possibly with +/-)
  c. fat percentage
  d. weight
7. Be able to add Ram with ear mark number and origin
8. Potentially divide sheep into flocks
9. Get statistics for each Sau on number of lambs, quality, fat, weight per/for
   all years
10. More statistics for all Sau per/for all years.
