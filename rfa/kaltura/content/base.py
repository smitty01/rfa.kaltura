"""Base Schemas and classes for Kaltura AT Classes"""
from Products.Archetypes import atapi

from AccessControl import ClassSecurityInfo

from rfa.kaltura.content import vocabularies

KalturaBaseSchema = atapi.Schema(
    (atapi.StringField('entryId',
                       searchable=0,
                       mode='r',
                       accesssor="getEntryId",
                       widget=atapi.ComputedWidget(label="Entry Id",
                                                 description="Entry Id set by Kaltura after upload (read only)",
                                                 visible = { 'edit' :'visible', 'view' : 'visible' },
                                                 i18n_domain="kaltura_video"),
                       ),
     
     atapi.StringField('playerId',
                       searchable=0,
                       accessor="getPlayer",
                       mutator="setPlayer", 
                       mode='rw',
                       default_method="getDefaultPlayerId",
                       #vocabulary_factory=getPlaylistPlayerVocabulary(),
                       #widget=atapi.SelectionWidget(label="Player",
                                                    #label_msgid="label_kplayerid_msgid",
                                                    #description="Choose the Video player to use",
                                                    #description_msgid="desc_kplayerid_msgid",
                                                    #i18n_domain="kaltura_video"),
                                                    #),
                      widget=atapi.StringWidget(label="Player Id",
                                                label_msgid="label_kplayerid_msgid",
                                                description="Enter the Player Id to use",
                                                description_msgid="desc_kplayerid_msgid",
                                                i18n_domain="kaltura_video"),
                      ),         
     
     atapi.StringField('partnerId',
                       searchable=0,
                       mode='rw',
                       default_method="getDefaultPartnerId",
                       widget=atapi.StringWidget(label="Partner Id",
                                                 label_msgid="label_kpartnerid_msgid",
                                                 description="Kaltura Partner Id (use default if unsure)",
                                                 description_msgid="desc_kpartnerid_msgid",
                                                 i18n_domain="kaltura_video"),
                       
                                             
                       ),
     )
     
)
    
    )


KalturaMetadataSchema = atapi.Schema(
    (atapi.LinesField('categories',
                      multiValued = True,
                      searchable=0,
                      required=False,
                      vocabulary="getCategoryVocabulary",
                      accessor="getCategories",
                      mutator="setCategories",
                      widget=atapi.MultiSelectionWidget(label="Categories",
                                                        label_msgid="label_kvideofile_categories",
                                                        description="Select video category(ies) this playlist will provide",
                                                        description_msgid="desc_kvideofile_categories",
                                                        i18n_domain="kaltura_video"),
                          ),       
    
     atapi.LinesField('tags',
                      multiValued = True,
                      searchable=0,
                      required=False,
                      vocabulary="getTagVocabulary",
                      accessor="getTags",
                      mutator="setTags",
                      widget=atapi.MultiSelectionWidget(label="Tags",
                                                        label_msgid="label_kvideofile_tags",
                                                        description="Select video tag(s) this playlist will provide ",
                                                        description_msgid="desc_kvideofile_title",
                                                        i18n_domain="kaltura_video"),
                      ),
     )
)

###XXX Todo: create base class ExternalMediaEntry 
##based off of http://www.kaltura.com/api_v3/testmeDoc/index.php?object=KalturaExternalMediaEntry

class KalturaContentMixin(object):
    
    security = ClassSecurityInfo()
    KalturaObject = None    
    categories = []
    tags = []    
    
    def __init__(self, oid, **kwargs):
        super(KalturaContentMixin, self).__init__(oid, **kwargs)
        self.KalturaObject = None

    security.declarePrivate("setKalturaObject")
    def setKalturaObject(self, obj):
        self.KalturaObject = obj
        self.KalturaObject.referenceId = self.UID()
        
    security.declarePublic("getEntryId")
    def getEntryId(self):
        if self.KalturaObject is not None:
            return self.KalturaObject.getId()
        else:
            return None     
        entryId = property(getEntryId)            
        
    security.declarePrivate('getDefaultPartnerId')
    def getDefaultPartnerId(self):
        return getCredentials()['PARTNER_ID']    

    def getTags(self):
        return self.tags
    
    def setTags(self, tags):
        self.tags = tags
        
    def getCategories(self):
        return self.keywords
    
    def setCategories(self, categories):
        self.categories = categories    

    def getTagVocabulary(self):
        return vocabularies.getTagVoculabulary()
        
    def getCategoryVocabulary(self):
        return vocabularies.getCategoryVoculabulary()
    