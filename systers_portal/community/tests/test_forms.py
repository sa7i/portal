from django.contrib.auth.models import User, Group
from django.test import TestCase


from community.forms import (EditCommunityForm, AddCommunityPageForm,
                             EditCommunityPageForm, PermissionGroupsForm,
                             RequestCommunityForm, EditCommunityRequestForm,
                             AddCommunityForm)
from community.models import Community, CommunityPage, RequestCommunity
from users.models import SystersUser


class RequestCommunityFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)

    def test_request_community_form(self):
        """Test Requestcommunity form"""
        invalid_data = {'name': 'Bar',
                        'slug': 'foo'}
        form = RequestCommunityForm(data=invalid_data, user=self.user)
        self.assertFalse(form.is_valid())
        valid_data = {'name': 'Bar', 'slug': 'bar', 'order': '1',
                      'is_member': 'Yes', 'email': 'foo@bar.com', 'type_community': 'Other',
                      'community_channel': 'Existing Social Media Channels ',
                      'demographic_target_count': 'Foobarbar', 'purpose': 'foopurpose',
                      'is_avail_volunteer': 'Yes', 'count_avail_volunteer': '15',
                      'content_developer': 'foobar', 'selection_criteria': 'foobarbar',
                      'is_real_time': 'foofoobar'
                      }
        form = RequestCommunityForm(data=valid_data, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.community_request = RequestCommunity.objects.get()
        self.assertEqual(self.community_request.name, 'Bar')
        self.assertEqual(self.community_request.slug, 'bar')
        self.assertEqual(self.community_request.user, self.systers_user)


class EditCommunityRequestFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community_request = RequestCommunity.objects.create(
            name="Foo", slug="foo", order=1, is_member='Yes', type_community='Other',
            community_channel='Existing Social Media Channels ',
            is_avail_volunteer='Yes', count_avail_volunteer=0,
            user=self.systers_user)

    def test_edit_community_form(self):
        """Test editing the request community form"""
        invalid_data = {'name': 'Bar',
                        'slug': 'foo'}
        form = RequestCommunityForm(data=invalid_data, user=self.user)
        self.assertFalse(form.is_valid())
        data = {'name': 'Bar', 'slug': 'bar', 'order': '1',
                'is_member': 'Yes', 'email': 'foo@bar.com', 'type_community': 'Other',
                'community_channel': 'Existing Social Media Channels ',
                'demographic_target_count': 'Foobarbar', 'purpose': 'foopurpose',
                'is_avail_volunteer': 'Yes', 'count_avail_volunteer': '15',
                'content_developer': 'foobar', 'selection_criteria': 'foobarbar',
                'is_real_time': 'foofoobar'
                }
        form = EditCommunityRequestForm(
            data=data, instance=self.community_request)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.community_request.name, 'Bar')
        self.assertEqual(self.community_request.slug, 'bar')
        # Test if order of the request exists in Community
        self.community = Community.objects.create(name="FooBarComm", slug="foobar",
                                                  order=1,
                                                  admin=self.systers_user)
        form = EditCommunityRequestForm(
            data=data, instance=self.community_request)
        self.assertFalse(form.is_valid())
        # Test if slug of the request exists in Community
        self.community.slug = "bar"
        self.community.save()
        form = EditCommunityRequestForm(
            data=data, instance=self.community_request)
        self.assertFalse(form.is_valid())


class EditCommunityFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.systers_user)

    def test_edit_community_form(self):
        """Test community form"""
        data = {'name': 'Bar',
                'slug': 'bar',
                'order': 1,
                'admin': self.systers_user}
        form = EditCommunityForm(data=data, instance=self.community)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.community.name, 'Bar')
        self.assertEqual(self.community.slug, 'bar')


class AddCommunityFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)

    def test_add_community_form(self):
        """Test add Community Form"""
        invalid_data = {'name': 'Bar',
                        'slug': 'foo'}
        form = AddCommunityForm(data=invalid_data, admin=self.systers_user)
        self.assertFalse(form.is_valid())

        data = {'name': 'Bar',
                'slug': 'foo',
                'order': '1'}
        form = AddCommunityForm(data=data, admin=self.systers_user)
        self.assertTrue(form.is_valid())
        form.save()
        self.community = Community.objects.get()
        self.assertEqual(self.community.name, 'Bar')
        self.assertEqual(self.community.slug, 'foo')
        self.assertEqual(self.community.admin, self.systers_user)


class AddCommunityPageFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.systers_user)

    def test_add_community_page_form(self):
        """Test add CommunityPage form"""
        invalid_data = {'title': "something"}
        form = AddCommunityPageForm(data=invalid_data, author=self.user,
                                    community=self.community)
        self.assertFalse(form.is_valid())

        data = {'slug': 'foo',
                'title': 'Foo',
                'order': 1,
                'content': "Rainbows and ponies"}
        form = AddCommunityPageForm(data=data, author=self.user,
                                    community=self.community)
        self.assertTrue(form.is_valid())
        form.save()
        resource = CommunityPage.objects.get()
        self.assertEqual(resource.title, 'Foo')
        self.assertEqual(resource.author, self.systers_user)


class EditCommunityPageFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.systers_user)

    def test_edit_community_page_form(self):
        """Test edit community page"""
        incomplete_data = {'slug': 'slug'}
        form = EditCommunityPageForm(data=incomplete_data)
        self.assertFalse(form.is_valid())

        page = CommunityPage.objects.create(slug="foo", title="Foo page",
                                            order=1,
                                            author=self.systers_user,
                                            content="Content",
                                            community=self.community)
        data = {'slug': 'bar',
                'title': 'Bar page',
                'order': 2,
                'content': "New content"}
        form = EditCommunityPageForm(instance=page, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        page = CommunityPage.objects.get()
        self.assertEqual(page.slug, 'bar')
        self.assertEqual(page.order, 2)
        self.assertEqual(page.title, "Bar page")


class PermissionGroupsFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='foo', password='foobar')
        self.systers_user = SystersUser.objects.get(user=self.user)
        self.community = Community.objects.create(name="Foo", slug="foo",
                                                  order=1,
                                                  admin=self.systers_user)

    def test_permissions_groups_form(self):
        """Test permission groups form"""
        invalid_form = PermissionGroupsForm(user=self.systers_user,
                                            community=self.community)
        self.assertFalse(invalid_form.is_valid())

        form = PermissionGroupsForm(user=self.systers_user, data={},
                                    community=self.community)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.initial, {})
        group = Group.objects.get(name="Foo: Community Moderator")
        self.assertEqual(form.groups, [group])
        form.save()
        self.assertFalse(self.systers_user.is_group_member(group))

        self.systers_user.join_group(group)
        form = PermissionGroupsForm(user=self.systers_user, data={},
                                    community=self.community,
                                    initial={'groups': [group.pk]})
        self.assertTrue(form.is_valid())
        self.assertCountEqual(form.initial['groups'], [group.pk])
        form.save()

        form = PermissionGroupsForm(user=self.systers_user,
                                    community=self.community,
                                    data={'groups': [group.pk]})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(self.systers_user.is_group_member(group))
