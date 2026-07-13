from django.contrib import admin
from .models import (
    InvestmentPlanSlide, SiteSetting, NavigationLink, PageContent,
    AccessibleSection, InvestmentPlanCard, AboutUs, AccessibleCard,
    TokenSaleSection, SwingSection, SwingContainer, ExchangeSection,
    ExchangeIcon, InvestmentPlan, BitcoinCalculator, FeatureItem,
    MarketInstrument
)

class AccessibleCardInline(admin.TabularInline):
    model = AccessibleCard
    extra = 5
    fields = ("title", "description", "image", "order")
    ordering = ("order",)

@admin.register(AccessibleSection)
class AccessibleSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")
    inlines = [AccessibleCardInline]

@admin.register(TokenSaleSection)
class TokenSaleSectionAdmin(admin.ModelAdmin):
    list_display = ("left_title", "right_title", "end_date", "contribution_received")

class SwingContainerInline(admin.TabularInline):
    model = SwingContainer
    extra = 4

@admin.register(SwingSection)
class SwingSectionAdmin(admin.ModelAdmin):
    inlines = [SwingContainerInline]
    list_display = ("highlight_text", "main_title")

class ExchangeIconInline(admin.TabularInline):
    model = ExchangeIcon
    extra = 4

@admin.register(ExchangeSection)
class ExchangeSectionAdmin(admin.ModelAdmin):
    inlines = [ExchangeIconInline]
    list_display = ("title",)

@admin.register(InvestmentPlanSlide)
class InvestmentPlanSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "button_text", "order")
    ordering = ("order",)

@admin.register(InvestmentPlanCard)
class InvestmentPlanCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)

@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "percentage_text", "duration_text", "min_amount", "max_amount", "button_text")
    search_fields = ("name", "percentage_text", "duration_text")
    ordering = ("min_amount",)

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("heading",)

@admin.register(BitcoinCalculator)
class BitcoinCalculatorAdmin(admin.ModelAdmin):
    list_display = ("title_first", "title_second", "default_currency")
    search_fields = ("title_first", "title_second")

@admin.register(FeatureItem)
class FeatureItemAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(SiteSetting)
admin.site.register(NavigationLink)
admin.site.register(PageContent)
admin.site.register(MarketInstrument)
