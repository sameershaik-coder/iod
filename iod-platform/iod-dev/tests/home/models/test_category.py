import pytest
from tests.test_classes import BaseTest
from django.contrib.auth.models import User
from apps.home.actions import instruments, networth, category, assetgroup
from apps.home.models import (
    BaseUnit,
    Networth,
    Category,
    AssetGroup,
    Instrument
)
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from apps.home.lib.exceptions import JsonableError
from apps.home.actions import instruments, networth as networth_actions

################################################################################################################################
# Category
################################################################################################################################


@pytest.mark.django_db
class Test_Category_Models(BaseTest):
    def test_category_allocation_base_unit_invalid(self,user,base_unit,networth)->None:
        
        category1 = category.do_create_category("MF",25, user)

        base_unit.value = -1
        base_unit.save()
        assert category1.get_category_allocation() == 1


################################################################################################################################
# Category Weightage
################################################################################################################################
@pytest.mark.django_db
class Test_Category_Model_Weightage(BaseTest):

    def test_do_multiple_category_weightage_hundred(self,user,networth)->None:
        
        c1 = category.do_create_category("MF1",25, user)
        c2 = category.do_create_category("MF2",25, user)
        c3 = category.do_create_category("MF3",25, user)
        c4 = category.do_create_category("MF4",25, user)


        assert Category.objects.get(name="MF1") == c1
        assert Category.objects.get(name="MF2") == c2
        assert Category.objects.get(name="MF3") == c3
        assert Category.objects.get(name="MF4") == c4
    
    def test_do_multiple_category_weightage_lessthan_hundred(self,user,networth)->None:
        c1 = category.do_create_category("MF1",25, user)
        c2 = category.do_create_category("MF2",25, user)
        c3 = category.do_create_category("MF3",25, user)
        c4 = category.do_create_category("MF4",24.99, user)


        assert Category.objects.get(name="MF1") == c1
        assert Category.objects.get(name="MF2") == c2
        assert Category.objects.get(name="MF3") == c3
        assert Category.objects.get(name="MF4") == c4
    
    def test_do_multiple_category_weightage_morethan_hundred(self,networth,user)->None:

        c1 = category.do_create_category("MF1",25, user)
        c2 = category.do_create_category("MF2",25, user)
        c3 = category.do_create_category("MF3",25, user)

        with pytest.raises(JsonableError):
            c4 = category.do_create_category("MF4",41, user)
        
        assert Category.objects.filter(name="MF4").count() == 0

        c4 = category.do_create_category("MF4",25, user)
        
        with pytest.raises(JsonableError):
            c5 = category.do_create_category("MF5",1, user)

        assert Category.objects.filter(name="MF5").count() == 0

################################################################################################################################
# Create Category
################################################################################################################################
@pytest.mark.django_db
class Test_Category_Model_Create(BaseTest):

    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_create_category_user_with_perm(self,user_types,networth,user,base_unit)->None:
        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)
        
        category1 = category.do_create_category("MF1",25, user)
        assert category1.networth.user == user
        assert category1.networth.baseunit == base_unit
        assert category1.networth == networth
        assert category1 == category1
        assert category1.name == "MF1"
        assert category1.weightage == 25

    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_create_category_user_without_perm(self,user_types,user,networth)->None:
        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)
        

        assert Category.objects.filter(name="MF1").count() == 0

        # Try to create with user with permission and success
        category.do_create_category("MF1",20,user)

        assert Category.objects.filter(name="MF1").count() == 1
    
    

################################################################################################################################
# Delete Category
################################################################################################################################
@pytest.mark.django_db
class Test_Category_Model_Delete(BaseTest):
    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_delete_category_user_with_perm(self,user_types,user,networth)->None:

        # update user based on scenario
        if user_types == "customer_user":
            self.initialize_user(user,False,False,True)
        elif user_types == "staff_user":
            self.initialize_user(user,False,True,True)
        elif user_types == "admin_user":
            self.initialize_user(user,True,False,True)

        category1 = category.do_create_category("MF",25, user)

        category.do_delete_category(category1,acting_user=user)

        qs = Category.objects.filter(name="MF")
        assert qs.count()==0

    @pytest.mark.parametrize("user_types", ["customer_user", "staff_user", "admin_user"])
    def test_do_delete_category_user_without_perm(self,user_types,user,networth)->None:
        # update user based on scenario
        if user_types == "customer_user":
            user.is_superuser = False
            user.is_staff = False
            user.save()
        elif user_types == "staff_user":
            user.is_superuser = False
            user.is_staff = True
            user.save()
        elif user_types == "admin_user":
            user.is_superuser = True
            user.is_staff = True
            user.save()
        category1 = category.do_create_category("MF",25, user)
        # create a new user 
        user_no_perm = User.objects.create_user(username='other_user', password='password')
        # Try to create category with different user and expect exception
        with pytest.raises(JsonableError):
            category.do_delete_category(category1,acting_user=user_no_perm)
        
        qs = Category.objects.filter(name="MF")
        assert qs.count() == 1
    
    def test_do_delete_category_adminuser_with_perm(self,user,networth)->None:
        category1 = category.do_create_category("MF",25, user)
        # create a new user 
        user_no_perm = User.objects.create_user(username='other_user', password='password')
        user_no_perm.is_superuser = True
        user_no_perm.is_active = True
        # Try to create category with different user and expect exception
        with pytest.raises(JsonableError):
            category.do_delete_category(category1,acting_user=user_no_perm)
        
        qs = Category.objects.filter(name="MF")
        assert qs.count() == 1

        

    
       