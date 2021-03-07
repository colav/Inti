MAColTypes = {}
MAColTypes['mag'] = {}

MAColTypes['mag']['long'] = ['EstimatedCitation',
 'JournalId',
 'FieldOfStudyId2',
 'AffiliationId',
 'RecommendedPaperId',
 'ConferenceInstanceId',
 'ChildFieldOfStudyId',
 'PaperFamilyCount',
 'AuthorId',
 'PaperCount',
 'FamilyId',
 'PaperId',
 'EntityId',
 'PaperReferenceId',
 'FieldOfStudyId',
 'ReferenceCount',
 'ConferenceSeriesId',
 'RelatedEntityId',
 'FieldOfStudyId1',
 'LastKnownAffiliationId',
 'CitationCount']

MAColTypes['mag']['int'] = ['AuthorSequenceNumber',
 'Rank',
 'RelationshipType',
 'Year',
 'ResourceType',
 'FamilyRank',
 'AttributeType',
 'RelatedType',
 'SourceType']

MAColTypes['mag']['float'] = ['Latitude',
'Longitude',
'Score',
'Rank']

MAColTypes['nlp'] = {}
MAColTypes['nlp']['long'] = ['PaperId','PaperReferenceId']

MAColTypes['advanced'] = {}
MAColTypes['advanced']['long'] = ['EntityId','RelatedEntityId','FieldOfStudyId','ChildFieldOfStudyId','PaperCount','PaperFamilyCount','CitationCount','PaperId','RecommendedPaperId','FieldOfStudyId1','FieldOfStudyId2']
MAColTypes['advanced']['int'] = ['RelatedType','AttributeType','Rank','Level']
MAColTypes['advanced']['float'] = ['Score']

MAColumnNames = {}
MAColumnNames['mag'] = {}
MAColumnNames['mag']['Authors'] = ['AuthorId', 'Rank', 'NormalizedName', 'DisplayName', 'LastKnownAffiliationId', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
MAColumnNames['mag']['Authors_indexes'] = ['AuthorId','LastKnownAffiliationId']

MAColumnNames['mag']['Affiliations'] = ['AffiliationId', 'Rank', 'NormalizedName', 'DisplayName', 'GridId', 'OfficialPage', 'WikiPage', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'Latitude', 'Longitude', 'CreatedDate']
MAColumnNames['mag']['Affiliations_indexes'] = ['AffiliationId','GridId']

MAColumnNames['mag']['PaperAuthorAffiliations'] = ['PaperId', 'AuthorId', 'AffiliationId', 'AuthorSequenceNumber', 'OriginalAuthor', 'OriginalAffiliation']
MAColumnNames['mag']['PaperAuthorAffiliations_indexes'] = ['PaperId','AuthorId','AffiliationId'] 

MAColumnNames['mag']['Papers'] = ['PaperId', 'Rank', 'Doi', 'DocType', 'PaperTitle', 'OriginalTitle', 'BookTitle', 'Year', 'Date', 'Publisher', 'JournalId', 'ConferenceSeriesId', 'ConferenceInstanceId', 'Volume', 'Issue', 'FirstPage', 'LastPage', 'ReferenceCount', 'CitationCount', 'EstimatedCitation', 'OriginalVenue', 'FamilyId', 'CreatedDate']
MAColumnNames['mag']['Papers_indexes'] = ['PaperId','JournalId','ConferenceSeriesId','ConferenceInstanceId','FamilyId']

MAColumnNames['mag']['PaperUrls'] = ['PaperId', 'SourceType', 'SourceUrl', 'LanguageCode']
MAColumnNames['mag']['PaperUrls_indexes'] = ['PaperId']

MAColumnNames['mag']['PaperResources'] = ['PaperId', 'ResourceType', 'ResourceUrl', 'SourceUrl', 'RelationshipType']
MAColumnNames['mag']['PaperResources_indexes'] = ['PaperId']

MAColumnNames['mag']['PaperReferences'] = ['PaperId', 'PaperReferenceId']
MAColumnNames['mag']['PaperReferences_indexes'] = ['PaperId', 'PaperReferenceId']

MAColumnNames['mag']['PaperExtendedAttributes'] = ['PaperId', 'AttributeType', 'AttributeValue']
MAColumnNames['mag']['PaperExtendedAttributes_indexes'] = ['PaperId']

MAColumnNames['mag']['Journals'] = ['JournalId', 'Rank', 'NormalizedName', 'DisplayName', 'Issn', 'Publisher', 'Webpage', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
MAColumnNames['mag']['Journals_indexes'] = ['JournalId']

MAColumnNames['mag']['ConferenceSeries'] = ['ConferenceSeriesId', 'Rank', 'NormalizedName', 'DisplayName', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'CreatedDate']
MAColumnNames['mag']['ConferenceSeries_indexes'] = ['ConferenceSeriesId']

MAColumnNames['mag']['ConferenceInstances'] = ['ConferenceInstanceId', 'NormalizedName', 'DisplayName', 'ConferenceSeriesId', 'Location', 'OfficialUrl', 'StartDate', 'EndDate', 'AbstractRegistrationDate', 'SubmissionDeadlineDate', 'NotificationDueDate', 'FinalVersionDueDate', 'PaperCount', 'PaperFamilyCount', 'CitationCount', 'Latitude', 'Longitude', 'CreatedDate']
MAColumnNames['mag']['ConferenceInstances_indexes'] = ['ConferenceInstanceId','ConferenceSeriesId']


MAColumnNames['nlp'] = {}
MAColumnNames['nlp']['PaperAbstractsInvertedIndex'] = ['PaperId','IndexedAbstract']
MAColumnNames['nlp']['PaperAbstractsInvertedIndex_indexes'] = ['PaperId']
MAColumnNames['nlp']['PaperCitationContexts'] = ['PaperId','PaperReferenceId','CitationContext']
MAColumnNames['nlp']['PaperCitationContexts_indexes'] = ['PaperId','PaperReferenceId']

MAColumnNames['advanced'] = {}
MAColumnNames['advanced']['EntityRelatedEntities'] = ['EntityId','EntityType','RelatedEntityId','RelatedEntityType','RelatedType','Score']
MAColumnNames['advanced']['EntityRelatedEntities_indexes'] = ['EntityId','RelatedEntityId']
MAColumnNames['advanced']['FieldOfStudyChildren'] = ['FieldOfStudyId','ChildFieldOfStudyId']
MAColumnNames['advanced']['FieldOfStudyChildren_indexes'] = ['FieldOfStudyId','ChildFieldOfStudyId']
MAColumnNames['advanced']['FieldOfStudyExtendedAttributes'] = ['FieldOfStudyId','AttributeType','AttributeValue']
MAColumnNames['advanced']['FieldOfStudyExtendedAttributes_indexes'] = ['FieldOfStudyId']
MAColumnNames['advanced']['FieldsOfStudy'] = ['FieldOfStudyId','Rank','NormalizedName','DisplayName','MainType','Level','PaperCount','PaperFamilyCount','CitationCount','CreatedDate']
MAColumnNames['advanced']['FieldsOfStudy_indexes'] = ['FieldOfStudyId']
MAColumnNames['advanced']['PaperFieldsOfStudy'] = ['PaperId','FieldOfStudyId','Score']
MAColumnNames['advanced']['PaperFieldsOfStudy_indexes'] = ['PaperId','FieldOfStudyId']
MAColumnNames['advanced']['PaperRecommendations'] = ['PaperId','RecommendedPaperId','Score']
MAColumnNames['advanced']['PaperRecommendations_indexes'] = ['PaperId','RecommendedPaperId']
MAColumnNames['advanced']['RelatedFieldOfStudy'] = ['FieldOfStudyId1','Type1','FieldOfStudyId2','Type2','Rank']
MAColumnNames['advanced']['RelatedFieldOfStudy_indexes'] = ['FieldOfStudyId1','FieldOfStudyId2']

MACollectionNames = {}
MACollectionNames['mag'] = ['Authors','Affiliations','PaperAuthorAffiliations','Papers','PaperUrls','PaperResources','PaperReferences','PaperExtendedAttributes','Journals','ConferenceSeries','ConferenceInstances']
MACollectionNames['nlp'] = ['PaperAbstractsInvertedIndex','PaperCitationContexts']
MACollectionNames['advanced'] = ['EntityRelatedEntities','FieldOfStudyChildren','FieldOfStudyExtendedAttributes','FieldsOfStudy','PaperFieldsOfStudy','PaperRecommendations','RelatedFieldOfStudy'] 
