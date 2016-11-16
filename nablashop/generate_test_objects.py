from Scripts.pilprint import description

from .models import Category, Product

text = "Lorem ipsum dolor sit amet, sale accusam ut sit, dicam platonem gubergren sit an. Mucius denique eum et, " \
       "at summo soluta vix. Dicat mediocritatem ad vix. Qui offendit conceptam moderatius ne. Cu usu alterum " \
       "moderatius. Pri oratio appellantur et, errem delenit ei vis. \nappareat intellegat constituto quo, " \
       " an menandri argumentum qui. Animal maiestatis incorrupte in sea. Ea usu animal petentium. Qui quod " \
       "recusabo complectitur ne, inani integre equidem sit at.\n Has et solum fastidii, clita graecis vim ut. " \
       "Eos cu dicant regione, sed fabellas torquatos eu, duo ea mucius persius perpetua. Dicat accusam sea ex, " \
       "vix doming elaboraret eu. Vim ei solum regione, ad eros oratio convenire vix, omittam oporteat ea eam. " \
       "Sea intellegam liberavisse at. \nvero scaevola temporibus cu. Ad dicam soleat commune nam, an exerci " \
       "audiam sensibus vix, et ius iusto paulo honestatis. Melius vocibus habemus mea cu, est et everti " \
       "veritus interpretaris. No eos euripidis definitiones, vix facilis iudicabit te. Purto tempor interesset " \
       "ut vis. Mea unum iracundia ne, ei erant tantas eripuit vis, eum ut aeterno euripidis dissentiet. In etiam " \
       "nullam nam, duo ei nisl erat dicat, ei labitur instructior quo. \nquatos mediocritatem qui eu, in " \
       "timeam sensibus consulatu duo, ceteros volutpat maiestatis ei qui. Sit id natum augue omittam, duo at " \
       "congue consectetuer, etiam errem prompta eu mel. Sea ei soleat tritani. Ea quas adversarium duo, " \
       "iisque veritus accusata vel id, stet iusto inimicus ei usu. Ne dolorem pertinax has, nam ei nisl ornatus"


def create():

    daljer, _= Category.objects.get_or_create(name='Daljer', description='Her er masse daljer', pk=2)
    kompendier, _ = Category.objects.get_or_create(name='Kompendier', description='Her er masse kompendier', pk=3)

    for i in range(1,6):
        name = 'Dalje %d'
        dalje, _ = Product.objects.get_or_create(name=(name % i), category=daljer, pk=i, description=text)
        dalje.photo.name = 'product_photo/medal.jpg'
        dalje.save()

    for i in range(6,11):
        name = 'Kompendium %d'
        k, _ = Product.objects.get_or_create(name=(name % (i-5)), category=kompendier, pk=i, description=text)
        k.photo.name = 'product_photo/kompendium.jpg'
        k.save()


    print('Objects generated')

