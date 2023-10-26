from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile

class AuthTestCase(TestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.email = "testuser@amcor.com"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        UserProfile.objects.create(user=self.user, usergroup='regular', location='Location1')
        self.client.login(username=self.username,password=self.password)

    def test_user_profile_created(self):
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_user_profile_fields(self):
        profile = UserProfile.objects.first()
        self.assertEqual(profile.usergroup, 'regular')
        self.assertEqual(profile.location, 'Location1')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

    def test_login_fail(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)

    def test_inactive_user_cannot_login(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account_awaiting_authentication'))
    

    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser@amcor.com',
            'password1': 'password123',
            'first_name':'new',
            'last_name':'user',
            'password2': 'password123',
            'location': 'NewLocation'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to authentication page
        self.assertRedirects(response, reverse('account_awaiting_authentication'))
        
        new_user = User.objects.get(email='newuser@amcor.com')
        self.assertIsNotNone(new_user)
        self.assertFalse(new_user.is_active)
        
        new_profile = UserProfile.objects.get(user=new_user)
        self.assertEqual(new_profile.usergroup, 'regular')
        self.assertEqual(new_profile.location, 'NewLocation')

    def test_registration_with_invalid_email(self):
        response = self.client.post(reverse('register'), {
            'email': 'invalid_email@gmail.com',
            'first_name':'new',
            'last_name':'user',
            'password1': 'password123',
            'password2': 'password123',
            'location': 'NewLocation'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid input:')
    
    def test_registration_required_fields(self):
        form_data = {
                'email': 'required@amcor.com',
                'first_name':'new',
                'last_name':'user',
                'password1': 'password123',
                'password2': 'password123',
                'location': 'NewLocation'     
            }
        for key in form_data.keys():
            modified_data = form_data.copy()
            modified_data[key] = ''
            response = self.client.post(reverse('register'), modified_data)
            self.assertEqual(response.status_code, 200, f"leaving {key} blank gave status {response.status_code} when 200 was expected")
        
    
    def test_registration_duplicate_email(self):
        form_data = {
            'email': 'duplicate@amcor.com',
            'first_name':'new',
            'last_name':'user',
            'password1': 'password123',
            'password2': 'password123',
            'location': 'NewLocation'
        }
        self.client.post(reverse('register'),form_data)
        form_data2 = {
            'email': 'duplicate@amcor.com',
            'first_name':'new',
            'last_name':'user',
            'password1': 'password123',
            'password2': 'password123',
            'location': 'NewLocation2'
        }    
        response = self.client.post(reverse('register'),form_data2)
        count = User.objects.filter(email='duplicate@amcor.com').count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, 200, f"Got status {response.status_code} when 200 was expected")
        self.assertContains(response, 'Invalid input:')
    
    def test_update_profile(self):
        response = self.client.post(reverse('update_profile'), {
                'first_name':'Mark',
                'last_name':'Corrigan',
                'location': 'The Quantocks'     
            })
        self.assertEqual(response.status_code, 200)
        
        my_user = User.objects.get(email='testuser@amcor.com')
        self.assertIsNotNone(my_user,f"Could not find the user information")
        self.assertTrue(my_user.is_active,f"User has not been activated")
        self.assertEqual(my_user.first_name,"Mark")
        self.assertEqual(my_user.last_name,"Corrigan")
        
        my_profile = UserProfile.objects.get(user=my_user)
        self.assertEqual(my_profile.usergroup, 'regular')
        self.assertEqual(my_profile.location, 'The Quantocks')
    
    def test_update_profile_required_fields(self):
        form_data = {
                'first_name':'Mark',
                'last_name':'Corrigan',
                'location': 'NewLocation'     
            }
        for key in form_data.keys():
            modified_data = form_data.copy()
            modified_data[key] = ''
            response = self.client.post(reverse('update_profile'), modified_data)
            self.assertEqual(response.status_code, 200, f"leaving {key} blank gave status {response.status_code} when 200 was expected")