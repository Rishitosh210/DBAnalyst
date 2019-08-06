from __future__ import unicode_literals

from datetime import timedelta, datetime, time

from django.core.files.storage import FileSystemStorage
from django.core.validators import URLValidator
from django.db import models

from audtech_proj import settings


# Create your models here.

class CompanyInfo(models.Model):
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    user_id = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    post_code = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=254, null=True)
    web_address = models.TextField(validators=[URLValidator()], null=True, blank=True)
    phone_no = models.CharField(max_length=50, null=True, verbose_name="Contact Number")
    logo = models.ImageField(storage=fs, null=True, blank=True)

    class Meta:
        default_permissions = ()
        managed = True


class Engagement(models.Model):
    user_id = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=60, null=True, blank=True)
    company_type = models.CharField(max_length=60, null=True, blank=True)
    engagement_name = models.CharField(max_length=90, null=True, blank=True)
    Currency = models.CharField(verbose_name="Entity Currency", max_length=50, null=True, blank=True)
    financial_management_system = models.CharField(max_length=90, null=True, blank=True, verbose_name='System Name')
    fiscal_start_month = models.DateField(blank=True, null=True, verbose_name='Fiscal Start Date')
    fiscal_end_month = models.DateField(blank=True, null=True, verbose_name='Fiscal End Date')
    additional_info = models.TextField(blank=True, null=True)
    created_date = models.DateField(null=True, blank=True, auto_now_add=True)

    class Meta:
        permissions = (
            ("create_eng ", "Create Engagement"),
        )
        managed = True


class Mapping(models.Model):
    eng = models.CharField(max_length=50, blank=True, null=True)
    client = models.CharField(max_length=200, blank=True, null=True, verbose_name='Financial System')
    transaction_type = models.CharField(max_length=200, blank=True, null=True)
    final_field = models.CharField(max_length=200, blank=True, null=True, verbose_name='Audtech Field')
    source_filed = models.CharField(max_length=200, blank=True, null=True, verbose_name='System Field')
    column_no = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        default_permissions = ()
        managed = True


class FinalTable(models.Model):
    client = models.CharField(max_length=1000000, blank=True, null=True)
    engangement = models.CharField(max_length=1000000, blank=True, null=True)
    user_id = models.CharField(max_length=1000000, blank=True, null=True)
    Upload_Date = models.DateField(blank=True, null=True)
    SrNo = models.CharField(max_length=50, blank=True, null=True)
    JournalDate = models.DateTimeField(blank=True, null=True)
    JournalNumber = models.CharField(max_length=1000000, blank=True, null=True)
    JournalType = models.CharField(max_length=1000000, blank=True, null=True)
    DivisionCode = models.CharField(max_length=1000000, blank=True, null=True)
    StatusPostedUnposted = models.CharField(max_length=1000000, blank=True, null=True)
    PostingDate = models.DateTimeField(blank=True, null=True, verbose_name='Posting Date')
    TransactionType = models.CharField(max_length=1000000, blank=True, null=True)
    ReferenceNo = models.CharField(max_length=1000000, blank=True, null=True)
    AccountCategory = models.CharField(max_length=1000000, blank=True, null=True)
    MainAccountCode = models.CharField(max_length=1000000, blank=True, null=True)
    MainAccountName = models.CharField(max_length=1000000, blank=True, null=True)
    SubAccountCode = models.CharField(max_length=1000000, blank=True, null=True)
    SubAccountName = models.CharField(max_length=1000000, blank=True, null=True)
    Year = models.CharField(max_length=1000000, blank=True, null=True)
    GroupName = models.CharField(max_length=1000000, blank=True, null=True)
    ShortText = models.TextField(blank=True, null=True)
    TaxReference = models.CharField(max_length=1000000, blank=True, null=True)
    Splitbetweenheads = models.CharField(max_length=1000000, blank=True, null=True)
    CreatedBy = models.CharField(max_length=1000000, blank=True, null=True)
    AuthorisedBy = models.CharField(max_length=1000000, blank=True, null=True)
    CurrencyCode = models.CharField(max_length=1000000, blank=True, null=True)
    DebitAmount = models.FloatField(blank=True, null=True)
    CreditAmount = models.FloatField(blank=True, null=True)
    DebitAmountFC = models.FloatField(blank=True, null=True)
    CreditAmountFC = models.FloatField(blank=True, null=True)
    DocumentHeaderText = models.CharField(max_length=1000000, blank=True, null=True)
    EntityCode = models.CharField(max_length=1000000, blank=True, null=True)

    class Meta:
        permissions = (
            ("is_analytics", "Analytics"),
            ("is_read", "Only read"),
            ("is_import", "Import Data"),
        )

    @property
    def date_gaps(self):
        try:
            x = self.JournalDate - self.PostingDate
            if x > timedelta(days=10):
                return x
        except:
            pass

    # def RiskProfiling(self):

    @property
    def Notbalance(self):
        try:
            Balance = self.CreditAmountFC - self.DebitAmountFC
            if Balance != 0:
                return self.CreditAmountFC
        except:
            pass

    @property
    def ubuntu(self):
        string_date = str(self.JournalDate)
        dt = datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S')
        tme = dt.time()
        if tme != time():
            return string_date

    @classmethod
    def filter_client(cls, client, engage):
        return cls.objects.filter(client=client, engangement=engage)
