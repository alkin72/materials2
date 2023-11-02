from docs.models import Receipt, ReceiptDetail, RegisterReceipt, RegisterReceiptComposition
from . import forms


class Move:
        @staticmethod
        def move_receipt(self, ref):
                reg_compare = RegisterReceipt.objects.filter(receipt_id=self.pk, datetime=self.date)
                if not reg_compare:
                        rec = RegisterReceipt.objects.create(receipt_id=self.pk, datetime=self.date, note=self.note)
                        reg = RegisterReceipt.objects.get(register_receipt_id=rec.register_receipt_id)
                        # r = RegisterReceiptComposition.objects.filter(register_receipt=rec.register_receipt_id)
                        # r.delete()
                        new = ReceiptDetail.objects.filter(receipt_id=self.pk)
                        for item in new:
                                RegisterReceiptComposition.objects.create(register_receipt=reg, materials=item.materials, value=item.value,
                                                                          datetime=reg.datetime)
                else:
                        # переписать эту функцию для сохранения информации по всем изменениям рецепта
                        rec = RegisterReceipt.objects.filter(receipt_id=self.pk, datetime=self.date).order_by('datetime').last()
                        #reg = RegisterReceipt.objects.get(register_receipt_id=rec.register_receipt_id)

                        if rec.datetime == self.date:
                                r = RegisterReceiptComposition.objects.filter(register_receipt=rec.register_receipt_id)
                                r.delete()
                                rec.delete()
                        rec = RegisterReceipt.objects.create(receipt_id=self.pk, datetime=self.date, note=self.note)
                        reg = RegisterReceipt.objects.get(register_receipt_id=rec.register_receipt_id)
                        new = ReceiptDetail.objects.filter(receipt_id=self.pk)
                        for item in new:
                                RegisterReceiptComposition.objects.create(register_receipt=reg, materials=item.materials, value=item.value,
                                                                          datetime=reg.datetime)


