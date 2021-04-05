from django.shortcuts import render, redirect
from organization.forms import OrganizationSetupForm, OfficeSetupFormSet, BirdFormSet
from organization.models import Organization, Office
from users.models import Account
from django.contrib.auth.decorators import login_required
import hashlib
from django.views.generic import TemplateView


@login_required
def organization_profile_view(request):
    return render(request, 'organization/organization_profile.html')


@login_required
def office_profile_view(request):
    return render(request, 'organization/office_profile.html')


@login_required
def team_invitation_view(request):
    # get organization_invite_link_append for the user associated organization
    print(Organization.objects.filter(id=request.user.organization_id).values('organization_invite_link_append')[0][
              'organization_invite_link_append'])

    # hash = hashlib.sha256("Hallo Manuel Wie geht es dir".encode())
    # print(hash.hexdigest())
    # print(hash('Manuel'))
    # print(hash('Floq AG'))
    # print(request.build_absolute_uri())
    return render(request, 'organization/team_invitation.html')

@login_required
def team_profile_view(request):
    return render(request, 'organization/team_profile.html')


# TODO only admins can use that and restrict to
@login_required
def organization_setup_view(request):
    # make sure that people with an organization cannot create another one
    if request.user.organization == None:
        # user does not have a organization

        context = {}
        form = OrganizationSetupForm()
        if request.method == 'POST':
            form = OrganizationSetupForm(request.POST)
            if form.is_valid():
                organization_names = form.cleaned_data['organization_name']
                organization_names_hash = hashlib.sha256(organization_names.encode())
                Organization.objects.create(organization_name=organization_names, creator_user_id=request.user.id,
                                            organization_invite_link_append=organization_names_hash.hexdigest())
                # Updating the new pk from the Organization Model into the Account Model
                Account.objects.filter(email__exact=request.user.email).update(
                    organization_id=Organization.objects.filter(organization_name=organization_names).values('id'))
                return redirect('office_setup')
            else:
                context['organization_setup_form'] = form

        else:
            context['organization_setup_form'] = form

        return render(request, 'organization/organization_setup.html', context)

    else:
        return redirect("overview")


@login_required
def office_setup_view(request):
    return render(request, 'organization/officesetup.html')




# @login_required
# def office_setup_view(request):
#     '''
#     Office setup when an organization does not have offices yet
#     '''

#     # make sure that only organizations without offices can access this page
#     # TODO so that homeoffice is excluded when visiting a 2nd time
#     if not Office.objects.filter(
#             organization_id=Organization.objects.filter(creator_user_id=request.user.id).values('id')[0]['id']):

#         # Then I create the organization's home office
#         Office.objects.create(office_name='Home office', office_location='Home office', office_capacity=100000,
#                         organization_id=Organization.objects.filter(creator_user_id=request.user.id).values('id')[0]['id'])

#         context = {}
#         form = OfficeSetupFormSet(queryset=Office.objects.none())
#         #Adding organization_names to context to display name in office_setup_view
#         context['organization_names'] = Organization.objects.filter(creator_user_id=request.user.id).values('organization_name')[0]['organization_name']
#         if request.method == 'POST':
#             form = OfficeSetupFormSet(request.POST)
#             if form.is_valid():
#                 # TODO not perfect yet, but works:
#                 # - add delete rows to insert
#                 # - check how much rows are filled and then based on that do for loop or not
#                 for f in form:
#                     cd = f.cleaned_data
#                     office_name     = cd.get('office_name')
#                     office_location = cd.get('office_location')
#                     office_capacity = cd.get('office_capacity')
#                     organization_id = Organization.objects.filter(creator_user_id=request.user.id).values('id')[0]['id']
#                     office = Office(office_name=office_name, office_location=office_location, office_capacity=office_capacity, organization_id=organization_id)
#                     office.save()

#                 # office_name = request.POST['office_name']
#                 # office_location = request.POST['office_location']
#                 # office_capacity = request.POST['office_capacity']
#                 # # print(office_name)
#                 # # print(office_location)
#                 # # print(office_capacity)
#                 # # print(Organization.objects.filter(creator_user_id = request.user.id).values('id')[0]['id'])
#                 # # organization_id = request.user.organization
#                 # Office.objects.create(office_name=office_name, office_location=office_location,
#                 #                       office_capacity=office_capacity)

#                 return redirect('team_invitation')
#             else:
#                 context['office_setup_formset'] = form
#         else:
#             context['office_setup_formset'] = form
#         return render(request, 'organization/office_setup.html', context)

#     else:
#         return redirect("overview")




# class BirdAddView(TemplateView):
#     template_name = "add_bird.html"
def BirdAddView(request):
    context = {}
    if request.method == 'GET':
        formset = BirdFormSet(queryset=Office.objects.none())
        context['bird_formset'] = formset
        return render(request, 'organization/add_bird.html', context)

    # # Define method to handle POST request
    # def post(self, *args, **kwargs):
    #     formset = BirdFormSet(data=self.request.POST)
    #
    #     # Check if submitted forms are valid
    #     if formset.is_valid():
    #         formset.save()
    #         return redirect(reverse_lazy("bird_list"))
    #
    #     return self.render_to_response({'bird_formset': formset})

# # make sure that people with an organization cannot create another one
# if request.user.organization == None:
#     # user does not have a organization
#
#     context = {}
#     form = OrganizationSetupForm()
#     if request.method == 'POST':
#         form = OrganizationSetupForm(request.POST)
#         if form.is_valid():
#             organization_names = form.cleaned_data['organization_name']
#             Organization.objects.create(organization_name = organization_names, creator_user_id = request.user.id)
#             # Updating the new pk from the Organization Model into the Account Model
#             Account.objects.filter(email__exact=request.user.email).update(organization_id=Organization.objects.filter(organization_name=organization_names).values('id'))
#             return redirect('team_invitation')
#         else:
#             context['organization_setup_form'] = form
#
#     else:
#         context['organization_setup_form'] = form
#
#     return render(request, 'organization/office_setup.html', context)
#
# else:
#     return redirect("overview")
