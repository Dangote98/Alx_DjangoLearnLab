from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from .views import PostViewSet,CommentViewSet
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Post
# Create your tests here.

#We now need to test these viewsets
#first, we create a class and set it up

class TestViews(APITestCase):
    def setUp(self):
        #first call the client object from apiclient class
        self.client = APIClient()
        #I then create a reverse for the urls
        #when using viewsets, we have an option to add -detail or -list. -detail is to see a single post, while list include post, put, and get
        self.posts_url = reverse('posts-list')
       
        self.comments_url = reverse('comments-list')
        #we first create the first user
        self.user1 = get_user_model().objects.create_user(
            username= 'Martin',
            email='martin@gmail.com',
            password='Martin1234.',
            date_of_birth = '2011-11-11',
            first_name = 'Martin',
            last_name = 'Junior'
            
        )
        #we then create the second user
        self.user2 = get_user_model().objects.create_user(
            username= 'Lawrence',
            email='lawrence@gmail.com',
            password='Lawrence1234.',
            date_of_birth = '2011-11-11',
            first_name = 'Lawrence',
            last_name = 'Junior'
            
        )
    #the first step is to test post creation.
    def test_post_creation(self):
        self.client.login(email='lawrence@gmail.com',password='Lawrence1234.')
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        response_data = response.json()
        print(response_data['title'])
        #I am checking in the jsonified data when title matches with what I have shared.
        self.assertEquals(response_data['title'],'This is the first test post')
    #next, I want to test whether a comment is created successfully.
    def test_comment_creation(self):
        self.client.login(email='lawrence@gmail.com',password='Lawrence1234.')
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
      #I have obtained the post
        post = Post.objects.get(title="This is the first test post")
        post_id = post.id #I have then obtained the id of the post
        print(post_id)
        response = self.client.post(self.comments_url,{
            "post_id": post_id, #I used post_id because It is referenced in the view as post_id where I get it from request data
            "content":"This is the content for this first comment"
        })
        
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
    def test_validate_length_of_title(self):
        self.client.login(email='lawrence@gmail.com',password='Lawrence1234.')
        response = self.client.post(self.posts_url,{
            "title":"This", #I am testing if when I type an title less than 5 characters I get an error.
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_400_BAD_REQUEST)
    #I have to now test put and then delete
    def test_update_post(self):
        #first, we login since the user is the author of the post
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        #first, we have to create a post
        response = self.client.post(self.posts_url,{
            "title":"This is the original post", #I am testing if when I type an title less than 5 characters I get an error.
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #get the id of the post
        post_id = response.data['id']
        #create a reverse url
        self.update_post_url = reverse('posts-detail',args=[post_id])
        #we then update this particular post
        response = self.client.put(self.update_post_url,{
            "title":"this is the updated version of the original post",
            "content":"This is the content for this updated post"
        })
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        print(response.data['title'])
        #we then assert to see if details and status code matches
    def test_update_comment(self):
        #first we login
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        #we then create a post to be associated with the comment
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we then obtain the id of the post
        post = Post.objects.get(title="This is the first test post")
        post_id = post.id #I have then obtained the id of the post
        print(post_id)
        #we first create the comment
        response = self.client.post(self.comments_url,{
            "post_id": post_id, #I used post_id because It is referenced in the view as post_id where I get it from request data
            "content":"This is the content for this first comment"
        })
        
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we then update the comment
        #we get the comment id
        comment_id = response.data['id']
        print(f"comment_id is {comment_id}")
        #create a reverse url for comment
        self.update_comment_url = reverse('comments-detail',args=[comment_id])
        #we then update this particular post
        response = self.client.put(self.update_comment_url,{
            "content":"This is the updated comment"
        })
        self.assertEquals(response.status_code,status.HTTP_200_OK)
        print(response.data['content'])
        #we then assert to see if details and status code matches
    def test_delete_post(self):
        #first we log in
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        #we then create the post to be deleted
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we get the id of the post
        post_id = response.data['id']
        #create a reverse url
        self.delete_post_url = reverse('posts-detail',args=[post_id])
        #we then perform delete
        response = self.client.delete(self.delete_post_url)
        self.assertEquals(response.status_code,status.HTTP_204_NO_CONTENT)
    def test_delete_comment(self):
        #first we login
        self.client.login(email='martin@gmail.com',password='Martin1234.')
        #we then create a post to be associated with the comment
        response = self.client.post(self.posts_url,{
            "title":"This is the first test post",
            "content":"This is the content for this test post"
        })
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we then obtain the id of the post
        post = Post.objects.get(title="This is the first test post")
        post_id = post.id #I have then obtained the id of the post
        print(post_id)
        #we first create the comment
        response = self.client.post(self.comments_url,{
            "post_id": post_id, #I used post_id because It is referenced in the view as post_id where I get it from request data
            "content":"This is the content for this first comment"
        })
        
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        #we then update the comment
        #we get the comment id
        comment_id = response.data['id']
        print(f"comment_id is {comment_id}")
        #create a reverse url for comment
        self.delete_comment_url = reverse('comments-detail',args=[comment_id])
        #we then update this particular post
        response = self.client.delete(self.delete_comment_url,)
        self.assertEquals(response.status_code,status.HTTP_204_NO_CONTENT)
