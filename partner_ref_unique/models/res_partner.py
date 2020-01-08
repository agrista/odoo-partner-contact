# Copyright 2016 Antonio Espinosa
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

<<<<<<< HEAD
    @api.constrains("ref", "is_company", "company_id")
=======
    # This related is needed in order to trigger the check when changing the
    # value on res.company
    partner_ref_unique = fields.Selection(
        related='company_id.partner_ref_unique', store=True,
    )

    @api.multi
    @api.constrains('ref', 'is_company', 'company_id', 'partner_ref_unique')
>>>>>>> 55fd4e49b (Store partner_ref_unique to allow triggering the error updating res.company)
    def _check_ref(self):
        for partner in self.filtered("ref"):
            # If the company is not defined in the partner, take current user company
            company = partner.company_id or self.env.company
            mode = company.partner_ref_unique
            # Don't raise when coming from contact merge wizard or no duplicates
            if not self.env.context.get("partner_ref_unique_merging") and (
                mode == "all" or (mode == "companies" and partner.is_company)
            ):
                domain = [
                    ("id", "!=", partner.id),
                    ("ref", "=", partner.ref),
                ]
                if mode == "companies":
                    domain.append(("is_company", "=", True))
                other = self.search(domain)
                if other:
                    raise ValidationError(
                        _("This reference is equal to partner '%s'")
                        % other[0].display_name
                    )
