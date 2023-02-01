# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #j'ai résolu la première question par plusieurs façons
    #1et2. première solution
    @api.constrains('order_line')
    def _check_exist_product_in_line(self):
        for order in self:
            products_in_lines = order.mapped('order_line.product_id')
            for product in products_in_lines:
                lines_count = len(order.order_line.filtered(lambda line: line.product_id == product))
                #4.L'alerte doit être visible uniquement pour les utilisateurs appartenant au groupe "manage prices" dans la catégorie "Sales Prices"
                #on doit bien vérifier la condition que l'utilisateur appartient à la groupe manage prices
                if lines_count > 1 and self.env.user.has_group('sk_sale.group_manage_prices'):
                    raise ValidationError(_("Vous avez ajouté l'article %s en double") % (product.name))
        return True

    #1et2. deuxième solution
    # @api.constrains('order_line')
    # def _check_exist_product_in_line(self):
    #     print('check product')
    #     for order in self:
    #         exist_product_list = []
    #         for line in order.order_line:
    #             if line.product_id.id in exist_product_list:
    #                 raise UserError(
    #                     _("Vous avez ajouté l'article (%s) en double") % (line.product_id.name))
    #             exist_product_list.append(line.product_id.id)


    #1et2.troisième solution j'ai ovrride la méthode create
    # @api.model
    # def create(self, vals):
    #     res = super(SaleOrder, self).create(vals)
    #     exist_product_list = []
    #     for line in res.order_line:
    #         if line.product_id.id in exist_product_list and self.env.user.has_group('sk_sale.group_manage_prices'):
    #             raise UserError(
    #                 _("Vous avez ajouté l'article %s en double") % (line.product_id.name))
    #         exist_product_list.append(line.product_id.id)
    #     return res

    #3. On peut retourner au lieu d'exception qui empèche la validation de devis, un message de warning
    # return {
    #     'warning': {
    #         'title': "Warning",
    #         'message': _("Vous avez ajouté l'article %s en double", line.product_id.name),
    #     }
    # }