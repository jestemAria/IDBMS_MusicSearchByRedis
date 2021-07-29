# DDBMS - Davoud Mohammadpour - by: Aria Radmehr

import redis
import terminaltables

request = redis.Redis(host='localhost', port=6379, db=0)
CURSOR_POINTER = '->'
PAGE_DIVIDER = '---------------------------------------------'
TABLE_DIVIDER = '|-----------------------------------------------------------------------------------------------------------|'
STR_SPR = ','
DIVIDER = '/'
CACHESAVECACHE = 'cachesavecache'


def main():
    show_menu()


def show_menu():
    print('---------------------------------------------')
    print('|          Welcome To Song Searcher         |')
    print('|            Enter The Number For           |')
    print('|               1-Register                  |')
    print('|               2-Sign In                   |')
    print('|               3-Upload A Song             |')
    print('|               4-Search A Song             |')
    print('---------------------------------------------')

    print(CURSOR_POINTER)
    a = input()

    if a == '1':
        register()
    elif a == '2':
        sign_in()
    elif a == '3':
        upload_song()
    elif a == '4':
        search_song()


def register():
    print(PAGE_DIVIDER)
    while 1:
        print('Pick A Username:')
        username = input()
        if username_checker(username):
            break
        else:
            print("This Username Already Picked! Try Another One")

    print('Set A Password:')
    password = input()
    print('First Name:')
    first_name = input()
    print('Last Name:')
    last_name = input()
    print('Email Address:')
    email = input()

    # Make Key & Value To Database
    key = username
    key2 = DIVIDER+username
    value = password + STR_SPR + first_name + STR_SPR + last_name + STR_SPR + email
    value2 = str(password)
    request.set(key, value)
    request.set(key2, value2)

    notification('Registered')
    show_menu()


def sign_in():
    print(PAGE_DIVIDER)
    while 1:
        print('Username:')
        en_username = input()
        if not username_checker(en_username):
            print('Password:')
            en_password = input()
            if password_checker(en_username, en_password):
                break
            else:
                print('Password Is Wrong!')
        else:
            print('No Username Found! Register Now')

    notification('Signed In')
    show_menu()


def upload_song():
    print(PAGE_DIVIDER)
    print('Title Of Song:')
    title = input()
    print('Name Of Artist:')
    artist = input()
    print('Title Of Album:')
    album = input()
    print('Release Year:')
    year = input()
    print('Genre Of Music:')
    genre = input()

    # Make Download Link
    download_link = 'http://songseracher.com/'+artist+'/'+title

    # Set Key By Title
    title_key = title
    title_value = '0' + STR_SPR + artist + STR_SPR + album + STR_SPR + year + STR_SPR + genre
    if is_not_existed(title):
        request.set(title_key, title_value)
    else:
        existed_value = decoder(title)
        new_title_value = existed_value + STR_SPR + title_value
        request.set(title_key, new_title_value)

    # Set Key By Artist
    artist_key = artist
    artist_value = '1' + STR_SPR + title + STR_SPR + album + STR_SPR + year + STR_SPR + genre
    if is_not_existed(artist):
        request.set(artist_key, artist_value)
    else:
        existed_value = decoder(artist)
        new_artist_value = existed_value + STR_SPR + artist_value
        request.set(artist_key, new_artist_value)

    # Set Key By Album
    album_key = album
    album_value = '2' + STR_SPR + title + STR_SPR + artist + STR_SPR + year + STR_SPR + genre
    if is_not_existed(album):
        request.set(album_key, album_value)
    else:
        existed_value = decoder(album)
        new_album_value = existed_value + STR_SPR + album_value
        request.set(album_key, new_album_value)

    # Set Key By Year
    year_key = year
    year_value = '3' + STR_SPR + title + STR_SPR + artist + STR_SPR + album + STR_SPR + genre
    if is_not_existed(year):
        request.set(year_key, year_value)
    else:
        existed_value = decoder(year)
        new_year_value = existed_value + STR_SPR + year_value
        request.set(year_key, new_year_value)

    # Set Key By Genre
    genre_key = genre
    genre_value = '4' + STR_SPR + title + STR_SPR + artist + STR_SPR + album + STR_SPR + year
    if is_not_existed(genre):
        request.set(genre_key, genre_value)
    else:
        existed_value = decoder(genre)
        new_genre_value = existed_value + STR_SPR + genre_value
        request.set(genre_key, new_genre_value)

    save_as_cache(title, artist, album, year, genre)

    notification('Upload Song')
    print('You Can Access The Song In : ' + download_link)
    print(PAGE_DIVIDER)
    show_menu()


def search_song():
    print(PAGE_DIVIDER)
    print('Search Bar:' + CURSOR_POINTER)
    string_search = input()
    print('Result/s:')

    if is_not_existed(string_search):
        if not similar_results(string_search):
            similar_results_2(string_search)
        # make every separated word link with(-)
    else:
        result = request.get(string_search)
        data = result.decode("utf-8")
        table_contents(data, string_search)


def username_checker(username):
    ask = request.get(username)
    if ask is None:
        return True
    else:
        return False


def password_checker(username, password):
    ask = request.get(DIVIDER+username)
    password_decode = ask.decode("utf-8")
    string = password
    if password_decode == string:
        return True
    else:
        return False


def is_not_existed(string):
    ask = request.get(string)
    if ask is None:
        return True
    else:
        return False


def decoder(string):
    row_data = request.get(string)
    decoded = row_data.decode("utf-8")
    return decoded


def notification(string):
    print(PAGE_DIVIDER)
    print('You Successfully', string, '!')
    print(PAGE_DIVIDER)


def table_contents(result, string_search):
    x = result.split(",")
    number = len(x)

    print('=============================================================================================================')
    print('|   #   |       Title       |       Artist      |       Album       |       Year        |        Genre      |')
    print('|=======|===================================================================================================|')

    if len(string_search) <= 3:
        string_search = '\t\t' + string_search + '\t\t\t'
    elif len(string_search) <= 5:
        string_search = '\t\t' + string_search + '\t\t'
    elif len(string_search) <= 7:
        string_search = '\t\t' + string_search + '\t\t'
    elif len(string_search) <= 10:
        string_search = '\t' + string_search + '\t\t'
    elif len(string_search) <= 14:
        string_search = '\t' + string_search + '\t'
    elif len(string_search) <= 17:
        string_search += '\t'

    for q in range(0, number):
        if len(x[q]) <= 3:
            x[q] = '\t\t' + x[q] + '\t\t\t'
        elif len(x[q]) <= 5:
            x[q] = '\t\t' + x[q] + '\t\t'
        elif len(x[q]) <= 7:
            x[q] = '\t\t' + x[q] + '\t\t'
        elif len(x[q]) <= 10:
            x[q] = '\t\t' + x[q] + '\t'
        elif len(x[q]) <= 14:
            x[q] = '\t' + x[q] + '\t'
        elif len(x[q]) <= 17:
            x[q] += '\t'

    counter = 1
    for p in range(0, number, 5):
        if x[0] == '\t\t0\t\t\t':
            print('|\t' + str(counter) + '\t|' + string_search + '|' + x[1+p] + '|' + x[2+p] + '|' + x[3+p] + '|' + x[4+p] + '|')
            print(TABLE_DIVIDER)
        if x[0] == '\t\t1\t\t\t':
            print('|\t' + str(counter) + '\t|' + x[1+p] + '|' + string_search + '|' + x[2+p] + '|' + x[3+p] + '|' + x[4+p] + '|')
            print(TABLE_DIVIDER)
        if x[0] == '\t\t2\t\t\t':
            print('|\t' + str(counter) + '\t|' + x[1+p] + '|' + x[2+p] + '|' + string_search + '|' + x[3+p] + '|' + x[4+p] + '|')
            print(TABLE_DIVIDER)
        if x[0] == '\t\t3\t\t\t':
            print('|\t' + str(counter) + '\t|' + x[1+p] + '|' + x[2+p] + '|' + x[3+p] + '|' + string_search + '|' + x[4+p] + '|')
            print(TABLE_DIVIDER)
        if x[0] == '\t\t4\t\t\t':
            print('|\t' + str(counter) + '\t|' + x[1+p] + '|' + x[2+p] + '|' + x[3+p] + '|' + x[4+p] + '|' + string_search + '|')
            print(TABLE_DIVIDER)
        counter = counter + 1

    print("Input 0 For Menu")
    key = input()
    if key == '0':
        show_menu()


def save_as_cache(title, artist, album, year, genre):

    cache = title + STR_SPR + artist + STR_SPR + album + STR_SPR + year + STR_SPR + genre
    if is_not_existed(CACHESAVECACHE):
        request.set(CACHESAVECACHE, CACHESAVECACHE)
    else:
        existed_cache = decoder(CACHESAVECACHE)
        new_cache = existed_cache + STR_SPR + cache
        request.set(CACHESAVECACHE, new_cache)


def similar_results(string_search):
    string_to_search = string_search[0:3]
    all_cache = decoder(CACHESAVECACHE)

    if all_cache.find(string_to_search) == -1:
        return False
    else:
        index = all_cache.find(string_to_search)
        close_cache = all_cache[0:index]

        number_of_commas = close_cache.count(",", 0, len(close_cache))
        splitted_cache = all_cache.split(",")
        the_similar_word = splitted_cache[number_of_commas]
        print("Nothing Found! But There Is A Similar Tag You Can Search For: " + '(' + the_similar_word + ')')


def similar_results_2(string_search):
    string_to_search_2 = string_search[len(string_search)-3:len(string_search)]
    all_cache = decoder(CACHESAVECACHE)

    if all_cache.find(string_to_search_2) == -1:
        print("Nothing Found! -Check Word Spelling")
        return
    else:
        index_2 = all_cache.find(string_to_search_2)
        close_cache_2 = all_cache[0:index_2]

        number_of_commas = close_cache_2.count(",", 0, len(close_cache_2))
        splitted_cache = all_cache.split(",")
        the_similar_word = splitted_cache[number_of_commas]
        print("Nothing Found! But There Is A Similar Tag You Can Search For: " + '(' + the_similar_word + ')')


main()
