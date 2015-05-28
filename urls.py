from django.conf.urls import patterns, url

from recipe import views

urlpatterns = patterns('',
    url(r'^$', views.RecipeHome, name='index'),
    
    url(r'^([0-9]+)$', views.RecipeView, name='recipe'),
    url(r'^small/([0-9]+)$', views.RecipeViewSmall, name='recipesmall'),
    
    url(r'^search$', views.RecipeSearch, name='recipesearch'),
    url(r'^editrecipe/([0-9]+)$', views.EditRecipe, name='editrecipe'),
    url(r'^deleterecipe/([0-9]+)$', views.DeleteRecipe, name='deleterecipe'),
    
    url(r'^uploadpic/([0-9]+)$', views.UploadPic, name='uploadpic'),
    
    url(r'^ingredient/([0-9]+)/([0-9]+)$', views.EditIngredient, name='ingredient'),
    url(r'^deleteingredient/([0-9]+)/([0-9]+)$', views.DeleteIngredient, name='deleteingredient'),
    url(r'^loadingred$', views.LoadIngred, name='loadingred'),
    
    url(r'^step/([0-9]+)/([0-9]+)$', views.EditStep, name='step'),
    url(r'^deletestep/([0-9]+)/([0-9]+)$', views.DeleteStep, name='deletestep'),
    
    url(r'^artist/([0-9]+)$', views.ViewArtist, name='artist'),
    
    url(r'^season/([0-9]+)/([0-9]+)$', views.EditSeason, name='season'),
    
    url(r'^menuplanner$', views.MenuPlanner, name='menuplanner'),
    url(r'^shoppinglist$', views.ShoppingList, name='shoppinglist'),
    
    url(r'^editmenu/([0-9]+)/([0-9]+)$', views.EditMenu, name='editmenu'),
    url(r'^removemenu/([0-9]+)/([0-9]+)$', views.RemoveMenu, name='removemenu'),
    
    url(r'^addshopping/([0-9]+)$', views.AddShoppingList, name='addshoppinglist'),
    url(r'^removeshoppinglist/([0-9]+)$', views.RemoveShoppingList, name='removeshoppinglist'),
    
    
)

