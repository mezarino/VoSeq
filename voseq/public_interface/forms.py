from django import forms
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet


class AdvancedSearchForm(ModelSearchForm):
    MALE = 'm'
    FEMALE = 'f'
    LARVA = 'l'
    WORKER = 'w'
    QUEEN = 'q'
    SEX_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
        (LARVA, 'larva'),
        (WORKER, 'worker'),
        (QUEEN, 'queen'),
    )

    DONT_KNOW = 'd'
    YES = 'y'
    NO = 'n'
    TYPE_SPECIES_CHOICES = (
        (DONT_KNOW, 'don\'t know'),
        (YES, 'yes'),
        (NO, 'no'),
    )

    SPREAD = 's'
    ENVELOPE = 'e'
    PHOTO = 'p'
    NONE = 'n'
    DESTROYED = 'd'
    LOST = 'l'
    VOUCHER_CHOICES = (
        (SPREAD, 'spread'),
        (ENVELOPE, 'in envelope'),
        (PHOTO, 'only photo'),
        (NONE, 'no voucher'),
        (DESTROYED, 'destroyed'),
        (LOST, 'lost'),
    )
    code = forms.CharField(label="Code in voseq", max_length=100, required=False)
    orden = forms.CharField(label="Order", max_length=100, required=False)
    superfamily = forms.CharField(label="Superfamily", max_length=100, required=False)
    family = forms.CharField(label="Family", max_length=100, required=False)
    subfamily = forms.CharField(label="Subfamily", max_length=100, required=False)
    tribe = forms.CharField(label="Tribe", max_length=100, required=False)
    subtribe = forms.CharField(label="Subtribe", max_length=100, required=False)
    genus = forms.CharField(label="Genus", max_length=100, required=False)
    species = forms.CharField(label="Species", max_length=100, required=False)
    subspecies = forms.CharField(label="Subspecies", max_length=100, required=False)
    country = forms.CharField(label="Country", max_length=100, required=False)
    specificLocality = forms.CharField(label="Specific Locality", max_length=250, required=False)
    typeSpecies = forms.ChoiceField(label="Type species", choices=TYPE_SPECIES_CHOICES, required=False)
    latitude = forms.FloatField(label="Latitude", required=False)
    longitude = forms.FloatField(label="Longitude", required=False)
    max_altitude = forms.IntegerField(label="Maximum altitude", required=False)
    min_altitude = forms.IntegerField(label="Minimum altitude", required=False)
    collector = forms.CharField(label="Collector", max_length=100, required=False)
    dateCollection = forms.DateField(label="Date of collection", required=False)
    extraction = forms.CharField(label="Extraction", max_length=50, help_text="Number of extraction event.", required=False)
    extractionTube = forms.CharField(label="Extraction tube", max_length=50, help_text="Tube containing DNA extract.", required=False)
    dateExtraction = forms.DateField(label="Date extraction", required=False)
    extractor = forms.CharField(label="Extractor", max_length=100, required=False)
    voucherLocality = forms.CharField(label="Voucher locality", max_length=200, required=False)
    publishedIn = forms.CharField(label="Published in", required=False)
    notes = forms.CharField(label="Notes", required=False)
    latesteditor = forms.CharField(label="Latest editor", required=False)
    hostorg = forms.CharField(label="Host organism", max_length=200, help_text="Hostplant or other host.", required=False)
    sex = forms.ChoiceField(label="Sex", choices=SEX_CHOICES, required=False)
    voucher = forms.ChoiceField(label="Voucher", choices=VOUCHER_CHOICES, required=False)
    voucherCode = forms.CharField(label="Alternative voucher code", max_length=100, help_text="Original code of voucher specimen.", required=False)
    determinedBy = forms.CharField(label="Determined by", max_length=100, help_text="Person that identified the taxon for this specimen.", required=False)
    auctor = forms.CharField(label="Author", max_length=100, help_text="Person that described this taxon.", required=False)

    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        sqs = super(AdvancedSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        keywords = {}
        for k, v in self.cleaned_data.items():
            if v != '' and v is not None:
                # remove after adding this to index
                if k == 'sex' or k == 'typeSpecies' or k == 'voucher' or k == 'models':
                    continue
                keywords[k] = v

        print(keywords)

        # Check if we got any input value to search from
        if bool(keywords) is True:
            sqs = sqs.filter(**keywords)

            return sqs