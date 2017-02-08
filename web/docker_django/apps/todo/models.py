from django.db import models

# General Note - this is a pet project with the intent to be fully
# functional across the globe. This is a self imposed requirement because I
# want the challenge.


# TODO
# create a correct engine (current line 18)
# revise methods on company

# Food Truck table additions:
#   Truck Group - freeform but only created by owner or operator
#   Add method for Avg rating to food truck table. Less expensive to recalc
#        with each review than each view.
#   Food_truck range/region
#       Allow for postal code and/or area code? Any others?
#       Create a region type or is that overkill?
# Possible tables to add (could grow while working on templates):
#   Company User - with supporting roles/permissions tables
#   State table - consider rename of `state`
# TESTING


# Changed:
# Added general tables:
#   Country table
#       Country should have a few preferred languages? If so,
#       that's still another table and lookup
#   Postal code table - with table for distance between postal codes
# Add company_division to company_address as optional?
# Add menu_item's price should be on a per truck basis
# Food Truck table additions:
#   Fare table with table to map between
#   Price Range table with table to map between
#   Localized tag-line/blurb - related to truck_list.html
#   User rating table with table to map between
#   Truck status (Active, Inactive, Canceled, Flagged for delete, pending)
#   Follower table
#   Follower count on food_truck

# Canceled/Deferred:
# menu_item_truck's price should allow multiple currencies
# Consider splitting into base DB and dynamic - Research best practice
#   Config (e.g. languages, countries) would go into base
#   User updated information would go into dynamic

# Definitely Later:
#   Unique pageview count for food trucks(is this worth it? Or is follower count enough?)
#       Any one metric (even two - could be manipulated)

class Language(models.Model):
    """Listing of languages available for localization"""
    name = models.CharField(max_length=20)

    class Meta(models.Model.Meta):
        db_table = 'language'


class LanguageLocalization(models.Model):
    """Allows language choices to be displayed in preferred language"""
    language_id_from = models.ForeignKey(Language, on_delete=models.CASCADE)
    language_id_to = models.ForeignKey(Language, on_delete=models.CASCADE)
    language_translation = models.CharField(max_length=20)

    class Meta(models.Model.Meta):
        db_table = 'language_localization'


class Currency(models.Model):
    currency_code = models.CharField(max_length=2)
    currency_name = models.CharField(max_length=12)
    currency_symbol = models.CharField(max_length=1)
    currency_unicode = models.CharField(max_length=10)

    class Meta(models.Model.Meta):
        db_table = 'currency'


class Country(models.Model):
    country_name_native = models.CharField(max_length=30)
    country_abbreviated_2_char = models.CharField(max_length=2)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)

    class Meta(models.Model.Meta):
        db_table = 'country'


class PostalCode(models.Model):
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    postal_value = models.CharField(max_length=10)

    class Meta(models.Model.Meta):
        db_table = 'postal_code'


class PriceRangeType(models.Model):
    range_icon_path = models.CharField(max_length=150, blank=True, null=True)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)

    class Meta(models.Model.Meta):
        db_table = 'price_range_type'


class Fare(models.Model):
    fare_name = models.CharField(max_length=20)

    class Meta(models.Model.Meta):
        db_table = 'fare'


class FareLocalized(models.Model):
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    fare_id = models.ForeignKey(Fare, on_delete=models.CASCADE)

    class Meta(models.Model.Meta):
        db_table = 'fare_localized'


class User(models.Model):
    user_name = models.CharField(max_length=80)
    email = models.CharField(max_length=60)
    picture_path = models.CharField(max_length=150)

    class Meta(models.Model.Meta):
        db_table = 'user'


class Company(models.Model):
    company_name_base = models.CharField(max_length=80)
    contact_name = models.CharField(max_length=40)
    contact_email = models.CharField(max_length=40)

    class Meta(models.Model.Meta):
        db_table = 'company'


class CompanyLocal(models.Model):
    """Company text information - name, blurb and longer marketing information,
    with localization.
    """
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    language_id = models.CharField(max_length=2)
    company_name_localized = models.CharField(max_length=80)
    company_description_short = models.CharField(max_length=40)
    company_description_long = models.CharField(max_length=300)
    img_path = models.CharField(max_length=150)

    class Meta(models.Model.Meta):
        db_table = 'company_local'


class CompanyAddressType(models.Model):
    """Table of various address types like billing, shipping, hq

    TODO:
    Add localization
    """
    name_base = models.CharField(max_length=20)

    class Meta(models.Model.Meta):
        db_table = 'company_address_type'


class CompanyAddressTypeLocal(models.Model):
    """Company Address Type - Human Readable localization"""
    company_address_type_id = models.ForeignKey(CompanyAddressType,
                                                on_delete=models.CASCADE)
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    type_name = models.CharField(max_length=20)
    type_description = models.CharField(max_length=50)

    class Meta(models.Model.Meta):
        db_table = 'company_address_type_local'


class CompanyDivision(models.Model):
    """Division of a company for any reason, geographic, logistical, etc.
    (Future-proofing) No localization needed.
    """
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_address_type_id = models.ForeignKey(CompanyAddressType,
                                                on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    contact_name = models.CharField(max_length=40)
    contact_email = models.CharField(max_length=40)
    note = models.CharField(max_length=40, blank=True, null=True)

    class Meta(models.Model.Meta):
        db_table = 'company_division'


class CompanyAddress(models.Model):
    """Allows multiple addresses for a company (e.g. multiple shipping
    destinations). No localization needed.
    """
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_division_id = models.ForeignKey(CompanyDivision,
                                            on_delete=models.CASCADE)
    company_address_type_id = models.ForeignKey(CompanyDivision,
                                                on_delete=models.CASCADE,
                                                blank=True,
                                                null=True)
    location_name = models.CharField(max_length=40)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=20)
    postal = models.CharField(max_length=8)
    country = models.CharField(max_length=2)
    note = models.CharField(max_length=50, blank=True, null=True)

    class Meta(models.Model.Meta):
        db_table = 'company_address'


class CompanyRelationshipType(models.Model):
    """Holds values for type of relationships - marketing, operators, etc"""
    name_base = models.CharField(max_length=30)

    class Meta(models.Model.Meta):
        db_table = 'company_relationship_type'


class CompanyRelationship(models.Model):
    """Tracks a company's relationship with other companies allowing
    owners, operators, marketing, and future proofs further concepts.

    This could be outgrown with significant traffic; currently out of scope.
    """
    company_id_from = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_id_to = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_relationship_type_id = models.ForeignKey(CompanyRelationshipType,
                                                     on_delete=models.CASCADE)

    class Meta(models.Model.Meta):
        db_table = 'company_relationship'


class CompanyRelationshipTypeLocal(models.Model):
    """Holds values for type of relationships - marketing, operators, etc"""
    language_id = models.ForeignKey(CompanyRelationshipType,
                                    on_delete=models.CASCADE)
    name_local = models.CharField(max_length=30)
    description_local = models.CharField(max_length=60)

    class Meta(models.Model.Meta):
        db_table = 'company_relationship_type_local'


class MenuItem(models.Model):
    """Holds all menu items, complete with localization"""
    name_base = models.CharField(max_length=30)
    img_path = models.CharField(max_length=150)
    menu_item_default_price = models.DecimalField(max_digits=9,
                                                  decimal_places=2)

    class Meta(models.Model.Meta):
        db_table = 'menu_item'


class MenuItemLocal(models.Model):
    """Menu Items - Human Readable localization
    Allows multilingual descriptions, which could be beneficial in various
    markets.
    """
    menu_item_id = models.ForeignKey(MenuItem,
                                     on_delete=models.CASCADE)
    language_id = models.ForeignKey(Language,
                                    on_delete=models.CASCADE)
    name_localized = models.CharField(max_length=30)
    description = models.CharField(max_length=150)

    class Meta(models.Model.Meta):
        db_table = 'menu_item_local'


class FoodTruckStatus(models.Model):
    name = models.CharField(max_length=20)

    class Meta(models.Model.Meta):
        db_table = 'food_truck_status'


class FoodTruckStatusLocalized(models.Model):
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    name_localized = models.CharField(max_length=20)

    class Meta(models.Model.Meta):
        db_table = 'food_truck_status_localized'


class FoodTruck(models.Model):
    name = models.CharField(max_length=40)
    food_truck_status_id = models.ForeignKey(FoodTruckStatus,
                                             on_delete=models.CASCADE)
    owner_id = models.ForeignKey(Company,
                                 on_delete=models.CASCADE)
    currency_id = models.ForeignKey(Currency,
                                    on_delete=models.CASCADE)
    price_range_type_id = models.ForeignKey(PriceRangeType,
                                            on_delete=models.CASCADE)
    price_range_val = models.DecimalField(max_digits=4,
                                          decimal_places=0,
                                          blank=True,
                                          null=True)
    review_score_average = models.DecimalField(max_digits=7,
                                               decimal_places=2,
                                               blank=True,
                                               null=True)
    review_score_median = models.DecimalField(max_digits=7,
                                              decimal_places=2,
                                              blank=True,
                                              null=True)
    img_path = models.CharField(max_length=150)
    subscriber_count = models.IntegerField()

    class Meta(models.Model.Meta):
        db_table = 'food_truck'


class FoodTruckMarketingLocalized(models.Model):
    """Contains various marketing messages, localized to language"""
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    marketing_line = models.CharField(max_length=200,
                                      blank=True,
                                      null=True)
    marketing_story = models.CharField(max_length=1500,
                                       blank=True,
                                       null=True)

    class Meta(models.Model.Meta):
        db_table = 'food_truck_marketing_localized'


class FoodTruckCompanyRelationship(models.Model):
    food_truck_id = models.ForeignKey(FoodTruck,
                                      on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company,
                                   on_delete=models.CASCADE)
    company_division_id = models.ForeignKey(CompanyDivision)
    models.ForeignKey(CompanyRelationshipType, on_delete=models.CASCADE)

    class Meta(models.Model.Meta):
        db_table = 'food_truck_company_relationship'


class FoodTruckMenuItem(models.Model):
    food_truck_id = models.ForeignKey(FoodTruck,
                                      on_delete=models.CASCADE)
    menu_item_id = models.ForeignKey(MenuItem,
                                     on_delete=models.CASCADE)
    menu_item_truck_price = models.DecimalField(max_digits=9,
                                                decimal_places=2,
                                                blank=True,
                                                null=True)

    class Meta(models.Model.Meta):
        db_table = 'food_truck_menu_item'


class FoodTruckFare(models.Model):
    fare_id = models.ForeignKey(FoodTruck, on_delete=models.CASCADE)
    food_truck_id = models.ForeignKey(Fare, on_delete=models.CASCADE)

    class Meta(models.Model.Meta):
        db_table = 'food_truck_fare'


class UserFoodTruckReview(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    food_truck_id = models.ForeignKey(FoodTruck, on_delete=models.CASCADE)
    review_score = models.DecimalField(max_digits=5, decimal_places=0)
    review_text = models.CharField(max_length=300)

    class Meta(models.Model.Meta):
        db_table = 'user_food_truck_review'


class UserFoodTruckSubscriber(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    food_truck_id = models.ForeignKey(FoodTruck, on_delete=models.CASCADE)

    class Meta(models.Model.Meta):
        db_table = 'user_food_truck_subscriber'


class UserFoodTruckSubscriberDay(models.Model):
    user_food_type_subscriber_id = models.ForeignKey(UserFoodTruckSubscriber,
                                                     on_delete=models.CASCADE)
    days_of_week = models.CharField(max_length=15)

    class Meta(models.Model.Meta):
        db_table = 'user_food_truck_subscriber_day'


class UserFoodTruckSubscriberDayPostal(models.Model):
    user_food_truck_subscriber_day_id = models.ForeignKey(UserFoodTruckSubscriberDay)
    postal_code = models.ForeignKey(PostalCode, on_delete=models.CASCADE)

    class Meta(models.Model.Meta):
        db_table = 'user_food_truck_subscriber_day_postal'
