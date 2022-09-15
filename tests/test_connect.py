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
