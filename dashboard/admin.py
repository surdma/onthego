import csv
from django.urls import path
from django.contrib import admin
from goshop.models import Category,Product,Brand,SubProduct,ProductType
from mptt.admin import DraggableMPTTAdmin
from django.forms import forms
from django.shortcuts import redirect, render

class CSVFormUploader(forms.Form):
    upload = forms.FileField()
    
 
@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin,admin.ModelAdmin):
    list_display = ("tree_actions","indented_title","parent",)
    search_fields = ("name","publish")
    prepopulated_fields= {"slug":("name",)}
    list_display_links = ("indented_title",)
    expand_tree_by_default = False

    def get_urls(self):
        urls = super().get_urls()
        upload_url = [
            path("upload-csv/", self.upload_csv),
        ]
        return upload_url + urls

    def upload_csv(self,request):
        if request.method == "POST":
            file = request.FILES["upload"]
            file_data = file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for data in csv_data:
                fields = data.split(",")
                created,uploaded = Category.objects.update_or_create(
                    name = fields[1],
                    slug = fields[2]
                )
                print(created)
            return redirect("..")


        form = CSVFormUploader()
        context = { "form":form}
        return render(request, "admin/goshop/category/upload_category/upload_csv.html", context=context)

    
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

class SubProductInline(admin.TabularInline):
    model = SubProduct


    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category","status")
    search_fields = ("name","category","status")
    prepopulated_fields= {"slug":("name",)}
    inlines = [SubProductInline]
    list_editable = ("status",)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)



# @admin.register(SubProduct)
# class SubProductAdmin(admin.ModelAdmin):
#     list_display = ("product","product_type")