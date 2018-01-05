from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
from .models import DFInput
import pandas as pd
import Funcs.diagramFuncs as draw
import Funcs.testFuncs as tst


def index_view(request):
    if request.method == 'POST' and request.FILES['myfile']:
        # traitement sur fichier
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        uid = get_random_string(length=5)
        filename = fs.save(uid + '_' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # creer des variables aidant
        file_path_to_read = uploaded_file_url[1:]
        file_name_html = filename[:-4] + ".html"
        file_path_to_html = "/index/templates/to_files/" + file_name_html
        file_path_to_html2 = "/media/to_files/" + file_name_html
        file_from_static = 'to_files/' + file_name_html
        desc_static = "to_files/" + uid + "_desc_file.html"
        desc_path = "/index/templates/" + desc_static

        # ouvrir le fichier avec pandas
        df = pd.read_csv(file_path_to_read)
        list_vars = list(df.columns.values)
        desc = df.describe()
        desc.to_html("." + desc_path)
        df.to_html("." + file_path_to_html)
        df.to_html("." + file_path_to_html2)

        fileName = request.POST.get("fileName")
        v_count = len(list_vars)
        vars_list = ",".join(list_vars)
        # ajouter au base de donnee
        b = DFInput(nom=fileName,
                    file_path=file_path_to_read,
                    vars=vars_list,
                    vars_count=v_count,
                    file_to_path=file_from_static,
                    describe_path=desc_static
                    )
        b.save()

        # last insert id
        last_f = DFInput.objects.latest('id')
        last_f = last_f.id

        fileName = fileName.capitalize()

        return render(request,
                      'index/manip.html',
                      {
                          'file_from_static': file_from_static,
                          'describe_path': desc_static,
                          'list_vars': list_vars,
                          'fileName': fileName,
                          'v_count': v_count,
                          'last_f': last_f,
                          'file_to_path': file_from_static
                      })
    return render(request, 'index/index.html')


def manip(request):
    if request.method == 'POST':
        list_vars = request.POST.getlist("list_vars")
        list_graph = request.POST.getlist("list_graph")
        file_id = request.POST.get("file_id")

        file_obj = DFInput.objects.get(pk=file_id)
        fileName = file_obj.nom
        v_count = file_obj.vars_count
        last_f = file_id

        file_path_to_read = file_obj.file_path
        df = pd.read_csv(file_path_to_read)

        divs = ''

        if list_graph[0] == 'bar':
            proofx = df[list_vars[0]]
            proofy1 = df[list_vars[1]]
            divs = draw.barplot(proofx, proofy1)

        elif list_graph[0] == 'c_bar':
            proofx = df[list_vars[0]]
            proofy1 = df[list_vars[1]]
            proofy2 = df[list_vars[2]]
            divs = draw.compare_bar(proofx, proofy1, proofy2)

        elif list_graph[0] == 'pie':
            proofx = df[list_vars[0]]
            proofy1 = df[list_vars[1]]
            divs = draw.pie(proofx, proofy1)

        elif list_graph[0] == 'c_pie':
            proofx = df[list_vars[0]]
            proofy1 = df[list_vars[1]]
            proofy2 = df[list_vars[2]]
            divs = draw.compare_pie(proofx, proofy1, proofy2)

        elif list_graph[0] == 'hist':
            proofx = df[list_vars[0]]
            divs = draw.histo(proofx)

        list_vars = file_obj.vars.split(',')
        describe_path = file_obj.describe_path
        file_to_path = file_obj.file_to_path

        fileName = fileName.capitalize()

        return render(request, 'index/manip.html', {
            'options_var': list_graph,
            'divs': divs,
            'list_vars': list_vars,
            'fileName': fileName,
            'v_count': v_count,
            'last_f': last_f,
            'describe_path': describe_path,
            'file_to_path': file_to_path
        })
    return render(request, 'index/manip.html')


def IC_test(request):
    if request.method == 'POST':
        list_vars = request.POST.getlist("list_vars")
        param = request.POST.getlist("param")
        alpha = request.POST.getlist("alpha")
        file_id = request.POST.get("file_id")

        var_display = list_vars[0]

        file_obj = DFInput.objects.get(pk=file_id)
        fileName = file_obj.nom
        v_count = file_obj.vars_count
        last_f = file_id
        describe_path = file_obj.describe_path
        file_to_path = file_obj.file_to_path

        file_path_to_read = file_obj.file_path
        df = pd.read_csv(file_path_to_read)

        divs = ''

        if param[0] == 'moy':
            proofx = df[list_vars[0]]
            divs = tst.intervale_moyenne(proofx, float(str(alpha[0])))

        elif param[0] == 'vari':
            proofx = df[list_vars[0]]
            divs = tst.intervale_variance(proofx, float(str(alpha[0])))

        list_vars = file_obj.vars.split(',')

        divs = 'Un intervalle de confiance de la variable "' + var_display + '" est: ' + divs
        fileName = fileName.capitalize()

        return render(request, 'index/manip.html', {
            'divs2': divs,
            'list_vars': list_vars,
            'fileName': fileName,
            'v_count': v_count,
            'last_f': last_f,
            'describe_path': describe_path,
            'file_to_path': file_to_path,
        })
    return render(request, 'index/manip.html')


def hypo(request):
    if request.method == 'POST':
        file_id = request.POST.get("file_id")
        list_vars = request.POST.getlist("list_vars")
        param = request.POST.getlist("param")
        alter = request.POST.getlist("alter")

        var_display = list_vars[0]

        file_obj = DFInput.objects.get(pk=file_id)
        fileName = file_obj.nom
        v_count = file_obj.vars_count
        last_f = file_id
        describe_path = file_obj.describe_path
        file_to_path = file_obj.file_to_path

        file_path_to_read = file_obj.file_path
        df = pd.read_csv(file_path_to_read)

        divs = ''
        param_f = ''

        if param[0] == 'norm':
            param_f = 'normal'
            if alter[0] == 'g':
                proofx = df[list_vars[0]]
                divs = tst.hynorm_gauche(proofx)
                param_f += ' gauche'
            elif alter[0] == 'd':
                proofx = df[list_vars[0]]
                divs = tst.hynorm_droite(proofx)
                param_f += ' droite'
            elif alter[0] == 'b':
                proofx = df[list_vars[0]]
                divs = tst.hynorm_bila(proofx)
                param_f += ' bilateral'

        elif param[0] == 'std':
            param_f = 'student'
            if alter[0] == 'g':
                proofx = df[list_vars[0]]
                divs = tst.hystudent_gauche(proofx)
                param_f += ' gauche'
            elif alter[0] == 'd':
                proofx = df[list_vars[0]]
                divs = tst.hystudent_droite(proofx)
                param_f += ' droite'
            elif alter[0] == 'b':
                proofx = df[list_vars[0]]
                divs = tst.hystudent_bila(proofx)

        elif param[0] == 'khi2':
            param_f = 'khi-deux'
            if alter[0] == 'g':
                proofx = df[list_vars[0]]
                divs = tst.hykhi_deux_gauche(proofx)
                param_f += ' gauche'
            elif alter[0] == 'd':
                proofx = df[list_vars[0]]
                divs = tst.hykhi_deux_droite(proofx)
                param_f += ' droite'
            elif alter[0] == 'b':
                proofx = df[list_vars[0]]
                divs = tst.hykhi_deux_bila(proofx)
                param_f += ' bilateral'

        list_vars = file_obj.vars.split(',')

        divs = "Test d'hypothese " + param_f + " sur \"" + var_display + "\": " + divs

        return render(request, 'index/manip.html', {
            'divs2': divs,
            'list_vars': list_vars,
            'fileName': fileName,
            'v_count': v_count,
            'last_f': last_f,
            'describe_path': describe_path,
            'file_to_path': file_to_path,
        })
    return render(request, 'index/manip.html')


def features(request):
    return render(request, 'index/features.html')
