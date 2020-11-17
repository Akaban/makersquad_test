from django.test import TestCase

from .models import Client, Invoice, InvoiceLine

class InvoiceAppTestCase(TestCase):
    def setUp(self):
        bryce = Client.objects.create(name="Bryce")
        romain = Client.objects.create(name="Romain")

        facture_bryce = Invoice.objects.create(client=bryce)
        facture_bryce_2 = Invoice.objects.create(client=bryce)
        facture_romain = Invoice.objects.create(client=romain)

        l1_facture_bryce = InvoiceLine.objects.create(
            invoice = facture_bryce,
            title = "Audit infrastructure existante 1h",
            iva_rate = 0.2,
            price_ht = 80,
            quantity = 5
        )
        
        l2_facture_bryce = InvoiceLine.objects.create(
            invoice = facture_bryce,
            title = "Mise en place d'une infrastructure du futur",
            iva_rate = 0.2,
            price_ht = 80,
            quantity = 7
        )


        l1_facture_romain = InvoiceLine.objects.create(
            invoice = facture_romain,
            title = "Analyse des besoins clients",
            iva_rate = 0.2,
            price_ht = 160,
            quantity = 7
        )
        
        l2_facture_romain = InvoiceLine.objects.create(
            invoice = facture_romain,
            title = "Développement d'un POC",
            iva_rate = 0.2,
            price_ht = 160,
            quantity = 7
        )
        
        l3_facture_romain = InvoiceLine.objects.create(
            invoice = facture_romain,
            title = "Connexion du POC aux interfaces client existantes",
            iva_rate = 0.2,
            price_ht = 160,
            quantity = 7
        )
        
        l1_facture_bryce_2 = InvoiceLine.objects.create(
            invoice = facture_bryce_2,
            title = "Brainstorm avec les équipes pour cadrer le projet",
            iva_rate = 0.2,
            price_ht = 80,
            quantity = 7
        )
        
        l2_facture_bryce_2 = InvoiceLine.objects.create(
            invoice = facture_bryce_2,
            title = "Développement d'un POC portant sur un nouveau moteur de recommandation",
            iva_rate = 0.2,
            price_ht = 80,
            quantity = 21
        )
        
        l3_facture_bryce_2 = InvoiceLine.objects.create(
            invoice = facture_bryce_2,
            title = "Mise en production",
            iva_rate = 0.2,
            price_ht = 80,
            quantity = 7
        )



    def test_clients_are_created(self):
        self.assertEqual(len(Client.objects.all()), 2)

        # Le client Romain existe
        self.assertEqual(len(Client.objects.all().filter(name="Romain")), 1)
        
        # Le client Bryce existe
        self.assertEqual(len(Client.objects.all().filter(name="Bryce")), 1)

    def invoices_are_created(self):

        # Il y a bien 3 factures
        self.assertEqual(len(Invoice.objects.all()), 3)
    
    def invoice_logic_is_working(self):

        facture_bryce_1 = Invoice.objects.all().filter(invoice_id=1)[0]
        facture_bryce_2 = Invoice.objects.all().filter(invoice_id=2)[0]
        facture_romain_1 = Invoice.objects.all().filter(invoice_id=3)[0]

        # La première facture de Bryce contient 2 lignes
        self.assertEqual(facture_bryce_1.get_number_of_lines, 2)

        # Le grand total de la première facture de Bryce est bien de 1152€
        self.assertEqual(facture_bryce_1.get_total_price, 1152)
        
        # La deuxième facture de Bryce contient 3 lignes
        self.assertEqual(facture_bryce_2.get_number_of_lines, 3)

        # Le grand total de la deuxième facture de Bryce est bien de 3360€
        self.assertEqual(facture_bryce_2.get_total_price, 3360)
        
        # La première facture de Romain contient 2 lignes
        self.assertEqual(facture_romain_1.get_number_of_lines, 3)
        
        # Le grand total de la première facture de Romain est bien de 4032€
        self.assertEqual(facture_romain_1.get_total_price, 4032)



