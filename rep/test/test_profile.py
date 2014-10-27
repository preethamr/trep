import datetime
import httplib
import json
import time
import tprofile 

def test_profile():

    u = tprofile.Profile('@rmahteerp').getProfile()
    assert u['id'] == 2865840637

    return "Passed"
    
print ("Profile retreival tests %s" % (test_profile(),))

def test_select():

    p = tprofile.Profile('@rmahteerp')
    

    # Filter valid

    start = datetime.datetime.fromtimestamp(10000)
    end = datetime.datetime.fromtimestamp(int(time.time() + 86400))
    f = { 'photo': 0, 'start': start, 'end':end, 'key':'retweet_count', 'reverse':0}
    assert len(p.getTweets(f)) == 3


    # Test filter inValid with same timestamp

    start = datetime.datetime.fromtimestamp(100)
    end = datetime.datetime.fromtimestamp(10000)
    f = { 'photo': 0, 'start': start, 'end':end, 'key':'retweet_count', 'reverse':0}
    assert len(p.getTweets(f)) == 0 

    # Test filter inValid offby1

    start = datetime.datetime.fromtimestamp(0)
    end = datetime.datetime.fromtimestamp(1)
    f = { 'photo': 0, 'start': start, 'end':end, 'key':'retweet_count', 'reverse':0}
    assert len(p.getTweets(f)) == 0

    # Test filter with photo 

    start = datetime.datetime.fromtimestamp(10000)
    end = datetime.datetime.fromtimestamp(int(time.time() + 86400))
    f = { 'photo': 1, 'start': start, 'end':end, 'key':'retweet_count', 'reverse':0}
    assert len(p.getTweets(f)) == 1

    # Test filter for order key validation

    start = datetime.datetime.fromtimestamp(10000)
    end = datetime.datetime.fromtimestamp(int(time.time() + 86400))
    f = { 'photo': 0, 'start': start, 'end':end, 'key':'some', 'reverse':0}
    assert len(p.getTweets(f)) == 3

    # Test filter for reverse order and default key

    start = datetime.datetime.fromtimestamp(10000)
    end = datetime.datetime.fromtimestamp(int(time.time() + 86400))
    f = { 'photo': 0, 'start': start, 'end':end, 'key':'some', 'reverse':0}
    tweets = p.getTweets(f)
    assert len(tweets) == 3
    assert tweets[0]['id'] == 523947457500028928

    return "Passed"

print ("Tweets filtering and ordering tests %s" % (test_select(),))


def test_score():

    p = tprofile.Profile('@rmahteerp')
    assert p.getScore() == 325

    p = tprofile.Profile('@marissamayer')
    assert p.getScore() > 400

    return "Passed"

print ("Profile score tests %s" % (test_score(),))


def test_http():
    # Simulate UI requests with a multi filter  with sorting request
    c =  httplib.HTTPConnection("127.0.0.1", "5000")
    c.request("GET", "/tweets/@rmahteerp?end=1414365725&key=created_at&photo=-1&reverse=0&start=946839278")
    r =  c.getresponse()
    d = r.read()

    # Assert HTTP response from the REST endpoint
    assert r.status == 200
    assert r.reason == 'OK'
    assert len(d) > 0
    j = json.loads(d)

    # Verify filtering
    assert len(j['tweets']) == 2

    # Verify sorting
    assert j['tweets'][0]['id'] == 523947457500028928

    # Verify safe handling of invalid filter request
    c =  httplib.HTTPConnection("127.0.0.1", "5000")
    c.request("GET", "/tweets/@6dc44a39bfe8cfa526478c3cfad7afc9?end=1414365725&key=created_at&photo=-1&reverse=0&start=946839278")
    r =  c.getresponse()
    d = r.read()

    # Assert HTTP response from the REST endpoint
    assert r.status == 200
    assert r.reason == 'OK'
    assert len(d) > 0
    j = json.loads(d)
    assert len(j['message']) > 0

    # Verify safe handling of invalid profile request
    c =  httplib.HTTPConnection("127.0.0.1", "5000")
    c.request("GET", "/profile/@6dc44a39bfe8cfa526478c3cfad7afc9?end=1414365725&key=created_at&photo=-1&reverse=0&start=946839278")
    r =  c.getresponse()
    d = r.read()

    # Assert HTTP response from the REST endpoint
    assert r.status == 200
    assert r.reason == 'OK'
    assert len(d) > 0
    j = json.loads(d)
    assert len(j['message']) > 0

    # Verify safe handling of invalid score request
    c =  httplib.HTTPConnection("127.0.0.1", "5000")
    c.request("GET", "/score/@6dc44a39bfe8cfa526478c3cfad7afc9?end=1414365725&key=created_at&photo=-1&reverse=0&start=946839278")
    r =  c.getresponse()
    d = r.read()

    # Assert HTTP response from the REST endpoint
    assert r.status == 200
    assert r.reason == 'OK'
    assert len(d) > 0
    j = json.loads(d)
    assert len(j['message']) > 0

    # Verify safe handling of valid score request
    c =  httplib.HTTPConnection("127.0.0.1", "5000")
    c.request("GET", "/score/@rmahteerp")
    r =  c.getresponse()
    d = r.read()

    # Assert HTTP response from the REST endpoint
    assert r.status == 200
    assert r.reason == 'OK'
    assert len(d) > 0
    j = json.loads(d)
    assert j['score'] == 325

    # Verify safe handling of valid profile request
    c =  httplib.HTTPConnection("127.0.0.1", "5000")
    c.request("GET", "/profile/@rmahteerp")
    r =  c.getresponse()
    d = r.read()

    # Assert HTTP response from the REST endpoint
    assert r.status == 200
    assert r.reason == 'OK'
    assert len(d) > 0
    j = json.loads(d)
    assert j['id'] == 2865840637 



    return "Passed"

print ("Profile http tests %s" % (test_http(),))
