# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from c7n.manager import resources
from c7n.query import QueryResourceManager, TypeInfo
from c7n.filters import ValueFilter
from c7n.utils import local_session, type_schema
from c7n.actions import Action
from c7n.filters.kms import KmsRelatedFilter

@resources.register('connect-instance')
class Connect(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'connect'
        enum_spec = ('list_instances', 'InstanceSummaryList', None)
        arn_type = 'instance'
        name = "InstanceAlias"
        id = "Id"


@Connect.filter_registry.register('instance-attribute')
class ConnectInstanceAttributeFilter(ValueFilter):
    """
    Filter Connect resources based on instance attributes

        :example:

    .. code-block:: yaml

            policies:

              - name: connect-instance-attribute
                resource: connect-instance
                filters:
                  - type: instance-attribute
                    key: Attribute.Value
                    value: true
                    attribute_type: CONTACT_LENS

    """

    schema = type_schema('instance-attribute', rinherit=ValueFilter.schema,
        required=['attribute_type'], **{'attribute_type': {'type': 'string'}})
    permissions = ('connect:DescribeInstanceAttribute',)
    annotation_key = 'c7n:InstanceAttribute'

    def process(self, resources, event=None):

        client = local_session(self.manager.session_factory).client('connect')
        results = []

        for r in resources:
            if self.annotation_key not in r:
                instance_attribute = client.describe_instance_attribute(InstanceId=r['Id'],
                                AttributeType=str.upper(self.data.get('attribute_type')))
                instance_attribute.pop('ResponseMetadata', None)
                r[self.annotation_key] = instance_attribute

            if self.match(r[self.annotation_key]):
                results.append(r)

        return results

    @Connect.action_registry.register("set-attributes")
    class SetAttributes(Action):
        """Set the attributes for the connect resources

        :example:

        .. code-block:: yaml

            policies:
              - name: connect-set-contact-lens
                resource: connect-instance
                filters:
                  - type: instance-attribute
                    key: Attribute.Value
                    value: false
                    attribute_type: CONTACT_LENS
                actions:
                  - type: set-attributes
                    attribute_type: CONTACT_LENS
                    value: true
              - name: connect-disable-contact-lens
                resource: connect-instance
                filters:
                  - type: instance-attribute
                    key: Attribute.Value
                    value: true
                    attribute_type: CONTACT_LENS
                actions:
                  - type: set-attributes
                    attribute_type: CONTACT_LENS
                    value: false
        """
        attributes = ["INBOUND_CALLS", "OUTBOUND_CALLS",
                      "CONTACTFLOW_LOGS", "CONTACT_LENS",
                      "AUTO_RESOLVE_BEST_VOICES", "USE_CUSTOM_TTS_VOICES",
                      "EARLY_MEDIA", "MULTI_PARTY_CONFERENCE",
                      "HIGH_VOLUME_OUTBOUND", "ENHANCED_CONTACT_MONITORING"]
        schema = type_schema("set-attributes", attribute_type={'anyOf': [{'enum': attributes},
                  {'type': 'string'}]}, value={}, required=["value", "attribute_type"])
        permissions = ("connect:UpdateInstanceAttribute",)

        def process(self, resources):
            client = local_session(self.manager.session_factory).client('connect')

            for r in resources:
                client.update_instance_attribute(InstanceId=r["Id"],
                    AttributeType=self.data.get("attribute_type"), Value=self.data.get("value"))


@resources.register('connect-campaign')
class ConnectCampaign(QueryResourceManager):

    class resource_type(TypeInfo):
        service = 'connectcampaigns'
        enum_spec = ('list_campaigns', 'campaignSummaryList', None)
        arn_type = 'campaign'
        name = "name"
        id = "id"


@ConnectCampaign.filter_registry.register('instance-config')
class ConnectCampaignInstanceConfigFilter(ValueFilter):
  schema = type_schema('instance-config', rinherit=ValueFilter.schema)    
  permissions = ('connectcampaigns:GetConnectInstanceConfig')
  annotation_key = 'c7n:InstanceConfig'
  
  def process(self, resources, event=None):
    client = local_session(self.manager.session_factory).client('connectcampaigns')
    results = []

    for r in resources:
        if self.annotation_key not in r:
            instance_config = client.get_connect_instance_config(
              connectInstanceId=r['connectInstanceId'])['connectInstanceConfig']
            r[self.annotation_key] = instance_config

        if self.match(r[self.annotation_key]):
            results.append(r)

    return results

    

@ConnectCampaign.filter_registry.register('kms-key')
class ConnectCampaignKmsFilter(KmsRelatedFilter):
  permissions = ('connectcampaigns:GetConnectInstanceConfig',)
  RelatedIdsExpression = 'keyArn'

  def get_related(self, resources):
      resource_manager = self.get_resource_manager()
      related_ids = self.get_related_ids(resources)
      if len(related_ids) < self.FetchThreshold:
          related = resource_manager.get_resources(list(related_ids))
      else:
          related = resource_manager.resources()
      related_map = {}
      # A resource's key property may point to an explicit ID or a key alias.
      # Be sure that a related key lookup covers both cases.
      for r in related:
          related_map[r['KeyId']] = r
          for alias in r.get('AliasNames', []):
              related_map[alias] = r
      return related_map

  def get_related_ids(self, resources):
    client = local_session(self.manager.session_factory).client('connectcampaigns')
    related_ids = []
    for r in resources:
      instance_config = client.get_connect_instance_config(
        connectInstanceId=r['connectInstanceId'])['connectInstanceConfig']
      related_ids.append(instance_config['encryptionConfig']['keyArn'])

    normalized_ids = []
    for rid in related_ids:
      normalized_ids.append(rid.rsplit('/', 1)[-1])

    return normalized_ids

