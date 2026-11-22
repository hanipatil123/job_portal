
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import JobCategory, Employer, JobPosting


class AdminModuleTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.admin_user = User.objects.create_superuser(
            username='testadmin',
            email='testadmin@example.com',
            password='TestPass123!xyz'
        )

        self.normal_user = User.objects.create_user(
            username='testuser',
            password='TestPass123!xyz'
        )

        self.category = JobCategory.objects.create(
            name='Python Developer',
            description='Python jobs'
        )

        self.employer = Employer.objects.create(
            company_name='Test Company',
            email='company@example.com'
        )

    # ======================================
    # 1. ADMIN LOGIN TEST
    # ======================================

    def test_admin_login_page(self):
        response = self.client.get(
            reverse('portal_admin:login')
        )
        self.assertEqual(response.status_code, 200)

    # ======================================
    # 2. ADMIN DASHBOARD TEST
    # ======================================

    def test_admin_dashboard(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(
            reverse('portal_admin:dashboard')
        )

        self.assertEqual(response.status_code, 200)

    # ======================================
    # 3. NORMAL USER ACCESS TEST
    # ======================================

    def test_normal_user_cannot_access_dashboard(self):
        self.client.force_login(self.normal_user)

        response = self.client.get(
            reverse('portal_admin:dashboard')
        )

        self.assertEqual(response.status_code, 302)

    # ======================================
    # 4. CATEGORY LIST TEST
    # ======================================

    def test_category_list(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(
            reverse('portal_admin:categories')
        )

        self.assertEqual(response.status_code, 200)

    # ======================================
    # 5. APPROVE EMPLOYER TEST
    # ======================================

    def test_approve_employer(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse(
                'portal_admin:approve_employer',
                args=[self.employer.pk]
            )
        )

        self.employer.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.employer.status,
            'approved'
        )

    # ======================================
    # 6. REJECT EMPLOYER TEST
    # ======================================

    def test_reject_employer(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse(
                'portal_admin:reject_employer',
                args=[self.employer.pk]
            )
        )

        self.employer.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.employer.status,
            'rejected'
        )

    # ======================================
    # 7. JOB POSTINGS PAGE TEST
    # ======================================

    def test_jobs_page(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(
            reverse('portal_admin:jobs')
        )

        self.assertEqual(response.status_code, 200)

    # ======================================
    # 8. REPORTS PAGE TEST
    # ======================================

    def test_reports_page(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(
            reverse('portal_admin:reports')
        )

        self.assertEqual(response.status_code, 200)

    # ======================================
    # 9. GUEST ACCESS SECURITY TEST
    # ======================================

    def test_guest_cannot_access_jobs(self):
        response = self.client.get(
            reverse('portal_admin:jobs')
        )

        self.assertEqual(response.status_code, 302)

    # ======================================
    # 10. NORMAL USER SECURITY TEST
    # ======================================

    def test_normal_user_cannot_access_users(self):
        self.client.force_login(self.normal_user)

        response = self.client.get(
            reverse('portal_admin:users')
        )

        self.assertEqual(response.status_code, 302)

    # ======================================
    # 11. EMPLOYER APPROVAL SECURITY TEST
    # ======================================

    def test_employer_approval_requires_post(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(
            reverse(
                'portal_admin:approve_employer',
                args=[self.employer.pk]
            )
        )

        self.assertEqual(response.status_code, 405)

        self.employer.refresh_from_db()

        self.assertEqual(
            self.employer.status,
            'pending'
        )

    # ======================================
    # 12. CATEGORY DELETE SECURITY TEST
    # ======================================

    def test_category_delete_requires_post(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(
            reverse(
                'portal_admin:category_delete',
                args=[self.category.pk]
            )
        )

        self.assertEqual(response.status_code, 405)

        self.assertTrue(
            JobCategory.objects.filter(
                pk=self.category.pk
            ).exists()
        )

    # ==================================
    # CATEGORY ADD TEST
    # ==================================

    def test_add_category(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse('portal_admin:category_add'),
            {
                'name': 'Java Developer',
                'description': 'Java development jobs'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            JobCategory.objects.filter(
                name='Java Developer'
            ).exists()
        )

    # ==================================
    # CATEGORY EDIT TEST
    # ==================================

    def test_edit_category(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse(
                'portal_admin:category_edit',
                args=[self.category.pk]
            ),
            {
                'name': 'Senior Python Developer',
                'description': 'Updated description'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.category.refresh_from_db()
        self.assertEqual(
            self.category.name,
            'Senior Python Developer'
        )

    # ==================================
    # CATEGORY DELETE TEST
    # ==================================

    def test_delete_category(self):
        self.client.force_login(self.admin_user)

        category_id = self.category.pk

        response = self.client.post(
            reverse(
                'portal_admin:category_delete',
                args=[category_id]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            JobCategory.objects.filter(
                pk=category_id
            ).exists()
        )

    # ==================================
    # JOB ADD TEST
    # ==================================

    def test_add_job(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse('portal_admin:job_add'),
            {
                'title': 'Django Developer',
                'employer': self.employer.pk,
                'category': self.category.pk,
                'location': 'Pune',
                'salary': '40000',
                'description': 'Django development',
                'status': 'active'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            JobPosting.objects.filter(
                title='Django Developer'
            ).exists()
        )

    # ==================================
    # JOB EDIT TEST
    # ==================================

    def test_edit_job(self):
        self.client.force_login(self.admin_user)

        job = JobPosting.objects.create(
            title='Python Developer',
            employer=self.employer,
            category=self.category,
            location='Pune',
            description='Python development',
            status='active'
        )

        response = self.client.post(
            reverse(
                'portal_admin:job_edit',
                args=[job.pk]
            ),
            {
                'title': 'Senior Python Developer',
                'employer': self.employer.pk,
                'category': self.category.pk,
                'location': 'Mumbai',
                'salary': '60000',
                'description': 'Updated job',
                'status': 'active'
            }
        )

        self.assertEqual(response.status_code, 302)

        job.refresh_from_db()

        self.assertEqual(
            job.title,
            'Senior Python Developer'
        )

    # ==================================
    # JOB DELETE TEST
    # ==================================

    def test_delete_job(self):
        self.client.force_login(self.admin_user)

        job = JobPosting.objects.create(
            title='Test Job',
            employer=self.employer,
            category=self.category,
            location='Pune',
            description='Test description'
        )

        job_id = job.pk

        response = self.client.post(
            reverse(
                'portal_admin:job_delete',
                args=[job_id]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            JobPosting.objects.filter(
                pk=job_id
            ).exists()
        )

