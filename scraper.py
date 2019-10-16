import requests
import json
import os.path
import sqlite3
from argparse import ArgumentParser

if not os.path.exists('downloads'):
    os.makedirs('downloads')
#USER_ID = 1211651
parser = ArgumentParser()
parser.add_argument('-m', '--min', action='store', help='Start scraping from x', type=int)
parser.add_argument("-i", "--userid", action="store", help="Only scrape user with this ID", type=int)
args = parser.parse_args()
url = 'https://unitedwardrobe.com/api/products'
#database
sqlite_file = 'data.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Data
             (ID, User_id, Sold, Gender, Category, subcategory, size, State, Brand, Colors, Price, Image, Images, Tag_one, Tag_two, Tag_three)''')
headers = {
    "Content-Type": "application/json",
    "X-Platform": "Web"
    }
if args.userid:
    USER_ID = args.userid

else:
    USER_ID = 1

if args.min:
    USER_ID = args.min
    print(args.min)
    
while USER_ID==USER_ID:
    print('ID=' + str(USER_ID))
    payload = {"limit":10000,"offset":0,"filters":{"user_id": USER_ID}}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    jsonresponse = r.json()
    print(jsonresponse)
    products = jsonresponse['products']
    if products:
        path= "downloads/" + str(USER_ID) +'/'
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed or the folder already exists " % path)
        else:
            print ("Successfully created the directory %s " % path)
        for product in jsonresponse['products']:
                img = product['images'].split(",")
                ID = product['id']
                User_id = product['user_id']
                Sold = product['sold']
                Gender = product['gender']
                Category = product['category']
                subcategory = product['subcategory']
                size = product['size']
                State = product['state']
                Brand = product['brand']
                Colors = product['colors']
                Price = product['price']
                Image = product['image']
                Images = product['images']
                tag_one = product['tag_one']
                tag_two = product['tag_two']
                tag_three = product['tag_three']
                path= "downloads/" + User_id +'/'
                img_path = path + Image
                
                
                print(img)
                

                if Image:
                    filepath2 = 'downloads/'+ str(User_id) +'/' + Image
                    req2 = requests.get(f"https://www.staticuw.com/image/product/xlarge/{Image}")
                if not os.path.isfile(filepath2):
                            with open(filepath2, 'wb') as f:
                                f.write(req2.content)
                            print(f"Image saved to {filepath2}")
                else:
                            print('File already exists, skipped.')
                if Images:
                    for images in img:
                        filepath = 'downloads/'+ str(User_id) +'/' + images
                        if not os.path.isfile(filepath):
                            req = requests.get(f"https://www.staticuw.com/image/product/xlarge/{images}")
                            params = (ID, User_id, Sold, Gender, Category, subcategory, size, State, Brand, Colors, Price, Image, filepath, tag_one, tag_two, tag_three)
                            c.execute("INSERT INTO Data(ID, User_id, Sold, Gender, Category, subcategory, size, State, Brand, Colors, Price, Image, Images, Tag_one, Tag_two, Tag_three)VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", params)
                            conn.commit()
                            with open(filepath, 'wb') as f:
                                f.write(req.content)
                            print(f"Image saved to {filepath}")
                        else:
                            print('File already exists, skipped.')
        
    if not products:
        print('User does not exists')
    if args.userid:
        exit()
    else:
        USER_ID+=1
conn.close()
