from django.test import TestCase
from .views import signup,login,UserProfileView
from rest_framework.test import APIRequestFactory,APIClient,APITestCase
from django.urls import reverse
from .models import CustomUser
from rest_framework import status
# Create your tests here.
#setUp allows us to initialize important details
class TestViews(APITestCase):
    def setUp(self):
        #we first get the client object from APIClient()
        #we then use reverse to reverse urls based on the assigned named
        self.client = APIClient()
        self.register_url = reverse('signup')
        self.login_url = reverse('login')
        self.profile_url = reverse('userprofile')
        self.auth_url = 'api_auth/'
        #here, I am creating a new user using the Customuser model
        self.new_user = CustomUser.objects.create_user(
            username="Michael",
            email="michael@gmail.com",
            date_of_birth = "2011-11-11",
            first_name="Michael",
            last_name= "James",
            password="Michael1234."
            
        )
    #I first tested the register of the new user
    def test_register_new_user(self):
        #I use the post method and pass the register url and the json details
        response = self.client.post(self.register_url,{
            "username":"Alex",
            "email":"alex@gmail.com",
            "password":"ALEX1234.",
            "first_name":"Alex",
            "last_name":"Guandaru",
            "date_of_birth":"2011-11-11",
            "bio":"",
            "profile_picture":""
            })
        #I then assertequals the response code I should expect
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        user = CustomUser.objects.get(email="alex@gmail.com")
        
        print(user.id)
        #here, I am trying to get specific details from the user, such as username and first name
        self.assertIn('username',response.data['user'])
        self.assertEquals(response.data['user']['username'],'Alex')
        self.assertIn('first_name',response.data['user'])
        self.assertEquals(response.data['user']['first_name'],'Alex')
        #here, I am testing logging in by using the post method and passing the login url and the asserting equals and in
    def test_login_new_user(self):
        response = self.client.post(self.login_url,{
            "email":"michael@gmail.com",
            "password":"Michael1234."
        })
        
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        self.assertIn("username",response.data["user"]) #we check whether username is in the response data under user section
        self.assertIn("last_name",response.data["user"]) #we check whether last_name is in the response data under user section
        self.assertEquals(response.data["user"]["username"],"Michael") #we check whether user can receive their data after login
        self.assertEquals(response.data["user"]["last_name"],"James") #we check whether user can receive their data after login
    #I then tested another new user
    def test_new_login_user(self) :
        self.user = self.client.post(self.register_url,{
            "username":"Ann",
            "email":"ann@gmail.com",
            "password":"Anne1234.",
            "first_name":"Ann",
            "last_name":"Michelle",
            "date_of_birth":"2011-11-11",
            "bio":"",
            "profile_picture":"",
            })
        response = self.client.post(self.login_url,{"email":"ann@gmail.com", "password":"Anne1234."})
        self.assertEquals(response.status_code,status.HTTP_200_OK) 
        token = response.data.get('token') #retrieves the token from user data
      
        print(token)  
        self.assertIsNotNone(token) #checks to see whether user token is empty
    #This was a nightmare because of the token. but I figured it out
    def test_user_profile_user(self):
        #we first login the user and get the token
        response = self.client.post(self.login_url, {
            'email': 'michael@gmail.com',
            'password': 'Michael1234.'
        })
        token = response.data.get('token')
        
        # Set the token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') #we use http_authorization
        response = self.client.get(reverse('userprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("email",response.data)
        # self.assertIn("username",response.data["user"])
        self.assertEquals(response.data["email"],"michael@gmail.com")
        # self.assertEquals(response.data['user']['username'],'Michael')
    #I tested another user here
    def test_another_user_profile(self):
        self.second_user = self.client.post(self.register_url,{
            "username":"Johnie",
            "email":"johnie@gmail.com",
            "password":"Johnie1234.",
            "first_name":"John",
            "last_name":"Lawrence",
            "date_of_birth":"2011-11-11",
            "bio":"This is a test",
            "profile_picture":"https://i.pinimg.com/originals/5a/72/9c/5a729ca9a4a4020c7090cc87665b7549.jpg"
            })
        response = self.client.post(self.login_url, {
            'email': 'johnie@gmail.com',
            'password': 'Johnie1234.'
        })
        token = response.data.get('token')
        # Set the token for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(reverse('userprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("email",response.data)
        # self.assertIn("username",response.data["user"])
        self.assertEquals(response.data["email"],"johnie@gmail.com")


