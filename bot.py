'''
Saba Heydaridoost

'''


from selenium import webdriver
import os
import time


class instaBot:
    def __init__(self, username_, password_):
        self.username = username_
        self.password = password_

        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.instaLink = 'https://www.instagram.com/'

        self.login()



    def login(self):
        self.driver.get('{}accounts/login/'.format(self.instaLink))
        
        try:
            self.driver.find_elements_by_xpath("//button[contains(text(), 'Accept')]")[0].click()
            
        except Exception:
            pass
        
        finally:
            time.sleep(2)
            
            self.driver.find_element_by_name("username").send_keys(self.username)
            self.driver.find_element_by_name("password").send_keys(self.password)
            
            self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
            
            time.sleep(3)

        

    def navigateUser(self, user):
        try:
            self.driver.get('{}{}/'.format(self.instaLink, user))
            time.sleep(5)
            
        except Exception:
            print('run code again!')

        
    def numberOfFollow(self, user):
        try:
            followers = self.driver.find_element_by_xpath("//li[2]/a/span").text
    
        except Exception:
            followers = 0

        try:
            followings = self.driver.find_element_by_xpath("//li[3]/a/span").text
            
        except Exception:
            followings = 0

        return followers, followings

    

    def numberOfPosts(self):
        intPosts = 0
       
        try:
            posts = self.driver.find_element_by_xpath('//li[1]/span/span').text
            intPosts = int(posts.replace(',', ''))

        except Exception:
            intPosts = 0
            
       
        return intPosts



    def likeAllPosts(self, user):
        self.navigateUser(user)

        time.sleep(3)
        
        posts = self.numberOfPosts()
        
        #opening the first post:
        self.driver.find_element_by_class_name("_9AhH0").click()

        time.sleep(3)
        
        for post in range(posts):
            
            #liking the post:
            self.driver.find_elements_by_class_name("wpO6b ")[2].click()
            
            #pressing next and move to the next post:
            try:
                self.driver.find_element_by_xpath("//a[contains(text(), 'Next')]").click()
            
            except Exception:
                break
            
            time.sleep(2)

   

    def followUser(self, user):
        self.navigateUser(user)
        
        try:
            self.driver.find_elements_by_xpath("//button[contains(text(), 'Follow')]")[0].click()
            
        except Exception:
            pass
            
        finally:
            time.sleep(3)

            followers, followings = self.numberOfFollow(user)

            return followers, followings


    def userFollowers(self, followers):
        followersButton = self.driver.find_element_by_xpath("//li[2]/a/span")
        followersButton.click()

        followersList = []

        print('followers : ', followers, type(followers))

        for i in range(10):
            try:
                follower = self.driver.find_elements_by_class_name('FPmhX ')[i]
                print('follower :{} '.format(i), follower.text)
                followersList.append(follower.text)

            except Exception:
                print('follower not readable!')
                pass
            
            time.sleep(2)

        time.sleep(3)
        
        return followersList



    def userFollowings(self, followings, user):
        self.navigateUser(user)

        time.sleep(3)
        
        followingsButton = self.driver.find_element_by_xpath("//li[3]/a/span")
        followingsButton.click()

        followingsList = []

        for i in range(10):
            try:
                following = self.driver.find_elements_by_class_name('FPmhX')[i]
                print('following :{} '.format(i), following.text)
                followingsList.append(following.text)
            
            except Exception:
                print('following not readable!')
                pass
            
            time.sleep(2)

        time.sleep(3)
        
        return followingsList

        
    def comment(self, user):
        content = 'very nice!'
        
        self.navigateUser(user)

        posts = self.numberOfPosts()
        
        #opening the first post:
        self.driver.find_element_by_class_name("_9AhH0").click()

        time.sleep(2)

        #comment button:
        self.driver.find_elements_by_class_name("wpO6b ")[3].click()

        time.sleep(2)

        #writing the text:
        self.driver.find_element_by_class_name("Ypffh").send_keys(content)

        time.sleep(1)

        #posting:
        self.driver.find_element_by_xpath("//button[contains(text(), 'Post')]").click()

        time.sleep(2)



if __name__ == '__main__':
    theBot = instaBot('username', 'password')

    followList = ['grimnsk', 'halloween_almaty']

    followFile = open('followFile.txt', mode = 'w')

    for user in followList:
        #Follows the user:
        followers, followings = theBot.followUser(user)

        #Making a list of followers and followings of the user:
        followersList = theBot.userFollowers(int(followers))
        followingsList = theBot.userFollowings(int(followings), user)

        #Writes number of followers and followings of the user in a file:
        followFile.write('user : {}, followers : {}, followings : {}\nfollowers list : {}\nfollowings list : {}\n'.format(
                          user, followers, followings, followersList, followingsList))

        postsLike = []
        
        postsLikes = theBot.likeAllPosts(user)

        theBot.comment(user)
        
        time.sleep(5)


    followFile.close()

    
