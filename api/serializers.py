from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from .models import UserProfile, Document, Order, Shop


class DocumentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.owner.username')
    class Meta:
        model = Document
        fields = ('doc_id','name', 'doc', 'owner')

class OrderSerializer(serializers.ModelSerializer):
    order_doc = serializers.ReadOnlyField(source='order_doc.name')
    shop = serializers.ReadOnlyField(source='shop.company_name')
    class Meta:
        model = Order
        fields = ('order_id', 'customer', 'order_doc','status','shop','comments')

class ShopSerializer(serializers.ModelSerializer):
    employee = serializers.ReadOnlyField(source='employee.username')
    owner = serializers.ReadOnlyField(source='owner.owner.username')
    class Meta:
        model = Shop
        fields = ('shop_id', 'employee', 'owner','shopName')



class UserSerializer(UserDetailsSerializer):
    company_name = serializers.CharField(source="userprofile.company_name", allow_blank=True)
    profile_picture = serializers.ImageField(source="userprofile.profile_picture", required=None)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('company_name','profile_picture',)  

    def update(self, instance, validated_data):
        # import ipdb; ipdb.set_trace();
        # validated_data2 = validated_data
        profile_data = validated_data.pop('userprofile', {})
        company_name = profile_data.get('company_name')
        profile_picture = profile_data.get('profile_picture')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = UserProfile()
        profile, created = UserProfile.objects.get_or_create(user=instance)
        if profile_data and (company_name or profile_picture):
            profile.company_name = company_name
            profile.profile_picture = profile_picture
            profile.save()
        else:
            profile.company_name = ''
            profile.profile_picture = ''
            profile.save()

        return instance