from django.db import models

# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="Bitnet.com")
    logo = models.ImageField(upload_to="images/", blank=True, null=True)
    buy_button_text = models.CharField(max_length=50, default="Buy Now")
    buy_button_url = models.CharField(max_length=100, default="/token/")

    def __str__(self):
        return self.site_name


class NavigationLink(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class PageContent(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    

class AccessibleSection(models.Model):
    title = models.CharField(max_length=200, default="Accessible for Everyone")
    subtitle = models.CharField(max_length=200, default="Crypto development accessible")

    class Meta:
        verbose_name = "Accessible Section"
        verbose_name_plural = "Accessible Sections"

    def __str__(self):
        return self.title
    

class AccessibleCard(models.Model):
    section = models.ForeignKey(
        AccessibleSection,
        related_name="cards",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="accessible_cards/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class TokenSaleSection(models.Model):
    left_title = models.CharField(max_length=200, default="Accessible for Everyone")
    left_subtitle = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=50, default="Sign Up")
    button_url = models.CharField(max_length=200, default="/register")

    right_title = models.CharField(max_length=200, default="The trading platform for the future")
    end_date = models.DateTimeField()  # when the countdown ends
    contribution_received = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    min_target = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    max_target = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Token Sale Section"
        verbose_name_plural = "Token Sale Sections"

    def __str__(self):
        return self.left_title
    

class SwingSection(models.Model):
    highlight_text = models.CharField(max_length=200, help_text="H4 text styled yellow on black background")
    main_title = models.CharField(max_length=200, help_text="H1 text, fifth word styled ash")
    canvas_text = models.CharField(max_length=200, blank=True, help_text="Optional text for the swinging canvas")

    def __str__(self):
        return self.highlight_text
    

class SwingContainer(models.Model):
    section = models.ForeignKey(SwingSection, related_name="containers", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class ExchangeSection(models.Model):
    title = models.CharField(max_length=255)   # h3 element
    description = models.TextField()           # p element
    main_image = models.ImageField(upload_to="exchange/")  # computer image

    def __str__(self):
        return self.title


class ExchangeIcon(models.Model):
    section = models.ForeignKey(ExchangeSection, related_name="icons", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="exchange/icons/")

    def __str__(self):
        return f"Icon for {self.section.title}"
    
    
class InvestmentPlan(models.Model):
    name = models.CharField(max_length=100)              
    percentage_text = models.CharField(max_length=100)  
    duration_text = models.CharField(max_length=100)    
    maturity_text = models.CharField(
        max_length=200, 
        default="Capital is returned on maturity"
    )
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    button_text = models.CharField(max_length=50, default="Sign Up")
    button_url = models.CharField(max_length=200, default="/register/")   

    class Meta:
        verbose_name = "Investment Plan"
        verbose_name_plural = "Investment Plans"

    def __str__(self):
        return self.name


class InvestmentPlanSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=50, default="Get Started")
    button_url = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    

class InvestmentPlanCard(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class AboutUs(models.Model):
    heading = models.CharField(max_length=200, default="WE ARE Bitnet")
    intro_text = models.TextField()
    mission_text = models.TextField(blank=True, null=True)
    advantages_text = models.TextField(blank=True, null=True)
    guarantees_text = models.TextField(blank=True, null=True)
    extra_text = models.TextField(blank=True, null=True)
    read_more_url = models.CharField(max_length=200, default="/features")

    def __str__(self):
        return self.heading
    
    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

class BitcoinCalculator(models.Model):
    title_first = models.CharField(max_length=50, default="BITCOIN")
    title_second = models.CharField(max_length=50, default="CALCULATOR")
    subtitle = models.CharField(max_length=200, default="Find out the current Bitcoin value with our easy-to-use converter.")
    default_currency = models.CharField(max_length=10, default="ARS")

    def __str__(self):
        return f"{self.title_first} {self.title_second}"
    
class FeatureItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='features/')

    def __str__(self):
        return self.title
    

class MarketInstrument(models.Model):
    ticker = models.CharField(max_length=10, default="UNKNOWN")  
    symbol = models.CharField(max_length=50, blank=True, null=True, default="")        
    price = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True, default=0.0)
    change_percent = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0.0)
    change_value = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True, default=0.0)
    bid = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True, default=0.0)
    ask = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True, default=0.0)
    high = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True, default=0.0)
    low = models.DecimalField(max_digits=12, decimal_places=6, blank=True, null=True, default=0.0)
    technical_rating = models.CharField(max_length=20, blank=True, null=True, default="Neutral")

    def __str__(self):
        return self.ticker


