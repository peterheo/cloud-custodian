from .common import BaseTest


class ConnectInstanceTest(BaseTest):

    def test_connect_instance_query(self):
        session_factory = self.replay_flight_data("test_connect_instance_query")
        p = self.load_policy(
            {
                "name": "connect-instance-query-test",
                "resource": "connect-instance"
            }, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_instance_attribute(self):
        session_factory = self.replay_flight_data("test_connect_instance_attribute")
        p = self.load_policy(
            {
                "name": "connect-instance-attribute-test",
                "resource": "connect-instance",
                "filters": [{
                    'type': 'instance-attribute',
                    'key': 'Attribute.Value',
                    'value': 'true',
                    'attribute_type': 'CONTACT_LENS'
                }]
            },
            session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)


class ConnectUserTest(BaseTest):

    def test_connect_user_query(self):
        session_factory = self.replay_flight_data("test_connect_user_query")
        p = self.load_policy(
            {
                "name": "connect-user-query-test",
                "resource": "connect-user"
            }, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_user_tag(self):
        session_factory = self.replay_flight_data("test_connect_user_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-user-tag-test",
                "resource": "connect-user",
                'actions': [{
                    'type': 'tag',
                    'key': 'abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['Arn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {'abcd': 'xyz'})

    def test_connect_user_remove_tag(self):
        session_factory = self.replay_flight_data("test_connect_user_remove_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-user-remove-tag-test",
                "resource": "connect-user",
                'actions': [{
                    'type': 'remove-tag',
                    'tags': ['TagMe']
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['Arn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {'abcd': 'xyz'})

    def test_connect_user_mark_for_op(self):
        session_factory = self.replay_flight_data("test_connect_user_mark_for_op")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-user-mark-for-op-test",
                "resource": "connect-user",
                'actions': [{
                    'type': 'mark-for-op',
                    'tag': 'custodian_cleanup',
                    'op': 'notify',
                    'days': 4
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['Arn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(
            tags.get('tags'),
            {'custodian_cleanup': 'Resource does not meet policy: notify@2022/09/11'}
        )

    def test_connect_user_tag_filter(self):
        session_factory = self.replay_flight_data("test_connect_user_tag_filter")

        p = self.load_policy(
            {
                "name": "connect-user-tag-filter-test",
                "resource": "connect-user",
                'filters': [{
                    'type': 'value',
                    'key': 'tag:abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)


class ConnectRoutingProfileTest(BaseTest):

    def test_connect_routing_profile_query(self):
        session_factory = self.replay_flight_data("test_connect_routing_profile_query")
        p = self.load_policy(
            {
                "name": "connect-routing-profile-query-test",
                "resource": "connect-routing-profile"
            }, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_routing_profile_tag(self):
        session_factory = self.replay_flight_data("test_connect_routing_profile_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-routing-profile-tag-test",
                "resource": "connect-routing-profile",
                'actions': [{
                    'type': 'tag',
                    'key': 'TagMe',
                    'value': 'true'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['RoutingProfileArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {'TagMe': 'true'})

    def test_connect_routing_profile_remove_tag(self):
        session_factory = self.replay_flight_data("test_connect_routing_profile_remove_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-routing-profile-remove-tag-test",
                "resource": "connect-routing-profile",
                'actions': [{
                    'type': 'remove-tag',
                    'tags': ['TagMe']
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['RoutingProfileArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {})

    def test_connect_routing_profile_mark_for_op(self):
        session_factory = self.replay_flight_data("test_connect_routing_profile_mark_for_op")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-routing-profile-mark-for-op-test",
                "resource": "connect-routing-profile",
                'actions': [{
                    'type': 'mark-for-op',
                    'tag': 'custodian_cleanup',
                    'op': 'notify',
                    'days': 4
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['RoutingProfileArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(
            tags.get('tags'),
            {'custodian_cleanup': 'Resource does not meet policy: notify@2022/09/11'}
        )

    def test_connect_routing_profile_tag_filter(self):
        session_factory = self.replay_flight_data("test_connect_routing_profile_tag_filter")

        p = self.load_policy(
            {
                "name": "connect-routing-profile-tag-filter-test",
                "resource": "connect-routing-profile",
                'filters': [{
                    'type': 'value',
                    'key': 'tag:abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)


class ConnectQueueTest(BaseTest):

    def test_connect_queue_query(self):
        session_factory = self.replay_flight_data("test_connect_queue_query")
        p = self.load_policy(
            {
                "name": "connect-queue-query-test",
                "resource": "connect-queue"
            }, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_queue_tag(self):
        session_factory = self.replay_flight_data("test_connect_queue_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-queue-tag-test",
                "resource": "connect-queue",
                'actions': [{
                    'type': 'tag',
                    'key': 'abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['QueueArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {'abcd': 'xyz'})

    def test_connect_queue_remove_tag(self):
        session_factory = self.replay_flight_data("test_connect_queue_remove_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-queue-remove-tag-test",
                "resource": "connect-queue",
                'actions': [{
                    'type': 'remove-tag',
                    'tags': ['abcd']
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['QueueArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {})

    def test_connect_queue_mark_for_op(self):
        session_factory = self.replay_flight_data("test_connect_queue_mark_for_op")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-queue-mark-for-op-test",
                "resource": "connect-queue",
                'actions': [{
                    'type': 'mark-for-op',
                    'tag': 'custodian_cleanup',
                    'op': 'notify',
                    'days': 4
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['QueueArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(
            tags.get('tags'),
            {'custodian_cleanup': 'Resource does not meet policy: notify@2022/09/11'}
        )

    def test_connect_queue_tag_filter(self):
        session_factory = self.replay_flight_data("test_connect_queue_tag_filter")

        p = self.load_policy(
            {
                "name": "connect-queue-tag-filter-test",
                "resource": "connect-queue",
                'filters': [{
                    'type': 'value',
                    'key': 'tag:abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)


class ConnectQuickConnectTest(BaseTest):

    def test_connect_quick_connect_query(self):
        session_factory = self.replay_flight_data("test_connect_quick_connect_query")
        p = self.load_policy(
            {
                "name": "connect-quick_connect-query-test",
                "resource": "connect-quick-connect"
            }, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_quick_connect_tag(self):
        session_factory = self.replay_flight_data("test_connect_quick_connect_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-quick_connect-tag-test",
                "resource": "connect-quick-connect",
                'actions': [{
                    'type': 'tag',
                    'key': 'abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['QuickConnectARN']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {'abcd': 'xyz'})

    def test_connect_quick_connect_tag_filter(self):
        session_factory = self.replay_flight_data("test_connect_quick_connect_tag_filter")

        p = self.load_policy(
            {
                "name": "connect-quick_connect-tag-filter-test",
                "resource": "connect-quick-connect",
                'filters': [{
                    'type': 'value',
                    'key': 'tag:abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_quick_connect_remove_tag(self):
        session_factory = self.replay_flight_data("test_connect_quick_connect_remove_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-quick_connect-remove-tag-test",
                "resource": "connect-quick-connect",
                'actions': [{
                    'type': 'remove-tag',
                    'tags': ['abcd']
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['QuickConnectARN']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {})

    def test_connect_quick_connect_mark_for_op(self):
        session_factory = self.replay_flight_data("test_connect_quick_connect_mark_for_op")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-quick_connect-mark-for-op-test",
                "resource": "connect-quick-connect",
                'actions': [{
                    'type': 'mark-for-op',
                    'tag': 'custodian_cleanup',
                    'op': 'notify',
                    'days': 4
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['QuickConnectARN']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(
            tags.get('tags'),
            {'custodian_cleanup': 'Resource does not meet policy: notify@2022/09/17'}
        )


class ConnectContactFlowTest(BaseTest):

    def test_connect_contact_flow_query(self):
        session_factory = self.replay_flight_data("test_connect_contact_flow_query")
        p = self.load_policy(
            {
                "name": "connect-contact-flow-query-test",
                "resource": "connect-contact-flow"
            }, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_contact_flow_tag(self):
        session_factory = self.replay_flight_data("test_connect_contact_flow_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-contact-flow-tag-test",
                "resource": "connect-contact-flow",
                'actions': [{
                    'type': 'tag',
                    'key': 'abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()

        self.assertEqual(len(resources), 1)

        arn = resources[0]['Arn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {'abcd': 'xyz'})

    def test_connect_contact_flow_tag_filter(self):
        session_factory = self.replay_flight_data("test_connect_contact_flow_tag_filter")

        p = self.load_policy(
            {
                "name": "connect-contact-flow-tag-filter-test",
                "resource": "connect-contact-flow",
                'filters': [{
                    'type': 'value',
                    'key': 'tag:abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()

        self.assertEqual(len(resources), 1)

    def test_connect_contact_flow_remove_tag(self):
        session_factory = self.replay_flight_data("test_connect_contact_flow_remove_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-contact-flow-remove-tag-test",
                "resource": "connect-contact-flow",
                'actions': [{
                    'type': 'remove-tag',
                    'tags': ['abcd']
                }]
            }, session_factory=session_factory
        )

        resources = p.run()

        self.assertEqual(len(resources), 1)
        arn = resources[0]['Arn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {})

    def test_connect_contact_flow_mark_for_op(self):
        session_factory = self.replay_flight_data("test_connect_contact_flow_mark_for_op")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-contact-flow-mark-for-op-test",
                "resource": "connect-contact-flow",
                'actions': [{
                    'type': 'mark-for-op',
                    'tag': 'custodian_cleanup',
                    'op': 'notify',
                    'days': 4
                }]
            }, session_factory=session_factory
        )

        resources = p.run()

        self.assertEqual(len(resources), 1)
        arn = resources[0]['Arn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(
            tags.get('tags'),
            {'custodian_cleanup': 'Resource does not meet policy: notify@2022/09/18'}
        )


class ConnectAgentStatusTest(BaseTest):

    def test_connect_agent_status_query(self):
        session_factory = self.replay_flight_data("test_connect_agent_status_query")
        p = self.load_policy(
            {
                "name": "connect-agent-status-query-test",
                "resource": "connect-agent-status"
            }, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 2)

    def test_connect_agent_status_tag(self):
        session_factory = self.replay_flight_data("test_connect_agent_status_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-agent-status-tag-test",
                "resource": "connect-agent-status",
                'actions': [{
                    'type': 'tag',
                    'key': 'abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 2)
        for r in resources:
            arn = r['AgentStatusARN']
            tags = client.list_tags_for_resource(resourceArn=arn)
            self.assertEqual(tags.get('tags'), {'abcd': 'xyz'})

    def test_connect_agent_status_tag_filter(self):
        session_factory = self.replay_flight_data("test_connect_agent_status_tag_filter")

        p = self.load_policy(
            {
                "name": "connect-agent-status-tag-filter-test",
                "resource": "connect-agent-status",
                'filters': [{
                    'type': 'value',
                    'key': 'tag:abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 2)

    def test_connect_agent_status_remove_tag(self):
        session_factory = self.replay_flight_data("test_connect_agent_status_remove_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-agent-status-remove-tag-test",
                "resource": "connect-agent-status",
                'actions': [{
                    'type': 'remove-tag',
                    'tags': ['abcd']
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 2)
        for r in resources:
            arn = r['AgentStatusARN']
            tags = client.list_tags_for_resource(resourceArn=arn)
            self.assertEqual(tags.get('tags'), {})

    def test_connect_agent_status_mark_for_op(self):
        session_factory = self.replay_flight_data("test_connect_agent_status_mark_for_op")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-agent-status-mark-for-op-test",
                "resource": "connect-agent-status",
                'actions': [{
                    'type': 'mark-for-op',
                    'tag': 'custodian_cleanup',
                    'op': 'notify',
                    'days': 4
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 2)
        for r in resources:
            arn = r['AgentStatusARN']
            tags = client.list_tags_for_resource(resourceArn=arn)
            self.assertEqual(
                tags.get('tags'),
                {'custodian_cleanup': 'Resource does not meet policy: notify@2022/09/18'}
            )


class ConnectHoursOfOperationTest(BaseTest):

    def test_connect_hours_of_operation_query(self):
        session_factory = self.replay_flight_data("test_connect_hours_of_operation_query")
        p = self.load_policy(
            {
                "name": "connect-hours-of-operation-query-test",
                "resource": "connect-hours-of-operation"
            }, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_hours_of_operation_tag(self):
        session_factory = self.replay_flight_data("test_connect_hours_of_operation_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-hours-of-operation-tag-test",
                "resource": "connect-hours-of-operation",
                'actions': [{
                    'type': 'tag',
                    'key': 'abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['HoursOfOperationArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {'abcd': 'xyz'})

    def test_connect_hours_of_operation_tag_filter(self):
        session_factory = self.replay_flight_data("test_connect_hours_of_operation_tag_filter")

        p = self.load_policy(
            {
                "name": "connect-hours-of-operation-tag-filter-test",
                "resource": "connect-hours-of-operation",
                'filters': [{
                    'type': 'value',
                    'key': 'tag:abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_hours_of_operation_remove_tag(self):
        session_factory = self.replay_flight_data("test_connect_hours_of_operation_remove_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-hours-of-operation-remove-tag-test",
                "resource": "connect-hours-of-operation",
                'actions': [{
                    'type': 'remove-tag',
                    'tags': ['abcd']
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['HoursOfOperationArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {})

    def test_connect_hours_of_operation_mark_for_op(self):
        session_factory = self.replay_flight_data("test_connect_hours_of_operation_mark_for_op")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-hours-of-operation-mark-for-op-test",
                "resource": "connect-hours-of-operation",
                'actions': [{
                    'type': 'mark-for-op',
                    'tag': 'custodian_cleanup',
                    'op': 'notify',
                    'days': 4
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['HoursOfOperationArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(
            tags.get('tags'),
            {'custodian_cleanup': 'Resource does not meet policy: notify@2022/09/18'}
        )


class ConnectPhoneNumberTest(BaseTest):
    def test_connect_phone_number_query(self):
        session_factory = self.replay_flight_data("test_connect_phone_number_query")
        p = self.load_policy(
            {
                "name": "connect-phone-number-query-test",
                "resource": "connect-phone-number"
            }, session_factory=session_factory
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_phone_number_tag(self):
        session_factory = self.replay_flight_data("test_connect_phone_number_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-phone-number-tag-test",
                "resource": "connect-phone-number",
                'actions': [{
                    'type': 'tag',
                    'key': 'abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['PhoneNumberArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {'abcd': 'xyz'})

    def test_connect_phone_number_tag_filter(self):
        session_factory = self.replay_flight_data("test_connect_phone_number_tag_filter")

        p = self.load_policy(
            {
                "name": "connect-phone-number-tag-filter-test",
                "resource": "connect-phone-number",
                'filters': [{
                    'type': 'value',
                    'key': 'tag:abcd',
                    'value': 'xyz'
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)

    def test_connect_phone_number_remove_tag(self):
        session_factory = self.replay_flight_data("test_connect_phone_number_remove_tag")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-phone-number-remove-tag-test",
                "resource": "connect-phone-number",
                'actions': [{
                    'type': 'remove-tag',
                    'tags': ['abcd']
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['PhoneNumberArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(tags.get('tags'), {})

    def test_connect_phone_number_mark_for_op(self):
        session_factory = self.replay_flight_data("test_connect_phone_number_mark_for_op")
        client = session_factory().client("connect")

        p = self.load_policy(
            {
                "name": "connect-phone-number-mark-for-op-test",
                "resource": "connect-phone-number",
                'actions': [{
                    'type': 'mark-for-op',
                    'tag': 'custodian_cleanup',
                    'op': 'notify',
                    'days': 4
                }]
            }, session_factory=session_factory
        )

        resources = p.run()
        self.assertEqual(len(resources), 1)
        arn = resources[0]['PhoneNumberArn']
        tags = client.list_tags_for_resource(resourceArn=arn)
        self.assertEqual(
            tags.get('tags'),
            {'custodian_cleanup': 'Resource does not meet policy: notify@2022/09/18'}
        )
