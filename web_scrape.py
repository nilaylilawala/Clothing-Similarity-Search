import requests
from bs4 import BeautifulSoup
import pickle

baseurl = "https://www.flipkart.com"

productlinks = []
unique_urls =[]

web_urls = ["https://www.flipkart.com/clothing-and-accessories/topwear/pr?sid=clo,ash&p[]=facets.ideal_for%255B%255D%3DMen&p[]=facets.ideal_for%255B%255D%3Dmen&otracker=categorytree&fm=neo%2Fmerchandising&iid=M_bb9803ec-9d97-42b1-b08a-669b5831638d_1_372UD5BXDFYS_MC.AHHHWF67UPNB&otracker=hp_rich_navigation_1_1.navigationCard.RICH_NAVIGATION_Fashion~Men%2527s%2BTop%2BWear~All_AHHHWF67UPNB&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_1_L2_view-all&cid=AHHHWF67UPNB&page={}",
            "https://www.flipkart.com/clothing-and-accessories/topwear/pr?sid=clo,ash&p[]=facets.ideal_for%255B%255D%3DWomen&p[]=facets.ideal_for%255B%255D%3Dwomen&otracker=categorytree&otracker=nmenu_sub_Women_0_Topwear&otracker=nmenu_sub_Women_0_Topwear&page={}",
            "https://www.flipkart.com/mens-footwear/pr?sid=osp,cil&otracker=nmenu_sub_Men_0_Footwear&otracker=nmenu_sub_Men_0_Footwear&page={}",
            "https://www.flipkart.com/womens-footwear/pr?sid=osp,iko&otracker=nmenu_sub_Women_0_Footwear&otracker=nmenu_sub_Women_0_Footwear&page={}",
            "https://www.flipkart.com/clothing-and-accessories/bottomwear/pr?sid=clo%2Cvua&otracker=categorytree&p%5B%5D=facets.ideal_for%255B%255D%3DMen&otracker=nmenu_sub_Men_0_Bottom%20wear&otracker=nmenu_sub_Men_0_Bottom%20wear&page={}",
            "https://www.flipkart.com/clothing-and-accessories/bottomwear/jeans/women-jeans/pr?sid=clo,vua,k58,4hp&otracker=categorytree&otracker=nmenu_sub_Women_0_Jeans&otracker=nmenu_sub_Women_0_Jeans&page={}"
            ]

# Web Scraping
for link in web_urls:
    for x in range(1, 5):
        k = requests.get(link.format(x)).text
        soup=BeautifulSoup(k,'html.parser')
        for a in soup.find_all("a",{"class":"_2UzuFa"}, href=True):
            url = a['href'].split("?pid")[0]
            if(url not in unique_urls):
                productlinks.append(url)
                unique_urls.append(url)
                # print(productlinks)

# Save the productlinks
with open("productlinks", "wb") as fp:
    pickle.dump(productlinks, fp)

