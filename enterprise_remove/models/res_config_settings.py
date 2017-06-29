# -*- coding: utf-8 -*-
#################################################################################
# Author      : SharpeIT Business Solutions (<www.sharp4IT.com>)
# Copyright(c): 2015-Present SharpeIT Business Solutions
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import api
from lxml import etree
from odoo.addons.base.res.res_config import ResConfigSettings


class ResConfigSettings(ResConfigSettings):

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):

        ret_val = super(ResConfigSettings, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )

        page_name = ret_val['name']
        doc = etree.XML(ret_val['arch'])

        queries = []
        if page_name == 'account settings':
            queries += [
                "//div[field[@name='module_account_reports' and \
                    @widget='upgrade_boolean']]",
                "//div[field[@name='module_account_reports_followup' and \
                    @widget='upgrade_boolean']]",
                "//div[field[@name='module_account_batch_deposit' and \
                    @widget='upgrade_boolean']]",
            ]

        queries += [
            "//div[div[field[@widget='upgrade_boolean']]] \
                /preceding-sibling::label[1]",
            "//div[div[field[@widget='upgrade_boolean']]]",
            "//div[field[@widget='upgrade_boolean']] \
                /preceding-sibling::label[1]",
            "//div[field[@widget='upgrade_boolean']]",
            "//field[@widget='upgrade_boolean']",
        ]

        for query in queries:
            for item in doc.xpath(query):
                item.getparent().remove(item)

        ret_val['arch'] = etree.tostring(doc)
        return ret_val
