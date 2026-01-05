from sqladmin import ModelView

from app.models import Note, ItemNote


class NoteAdmin(ModelView, model=Note):
	name = "Notas Fiscais"
	name_plural = "Notas Fiscais"
	icon = "fa fa-file-invoice-dollar"
	category = "Financeiro"
	category_icon = "fa fa-dollar-sign"

	can_create = False
	can_edit = True
	can_delete = True
	can_view_details = True

	page_size = 50
	page_size_options = [25, 50, 100, 200]

	column_list = [
		Note.id,
		Note.note_type,
		Note.note_number,
		Note.provider,
		Note.date_of_issue,
		Note.total_value,
		Note.created_at,
	]

	column_details_list = [
		Note.id,
		Note.note_type,
		Note.note_number,
		Note.series,
		Note.access_key,
		Note.issuer_cnpj,
		Note.issuer_city,
		Note.issuer_state,
		Note.total_value,
		Note.items,
	]

	column_labels = {
		Note.id: "ID",
		Note.note_type: "Tipo da Nota",
		Note.note_number: "Número da Nota",
		Note.series: "Série",
		Note.access_key: "Chave de Acesso",
		Note.issuer_cnpj: "CNPJ Emitente",
		Note.issuer_ie: "IE Emitente",
		Note.issuer_city: "Cidade Emitente",
		Note.issuer_state: "UF Emitente",
		Note.issuer_zip_code: "CEP Emitente",
		Note.nature_of_operation: "Natureza da Operação",
		Note.protocol_number: "Número do Protocolo",
		Note.date_of_issue: "Data de Emissão",
		Note.total_value: "Valor Total",
		Note.pdf_url: "URL do PDF",
		Note.pdf_file: "Arquivo PDF",
		Note.created_at: "Criado em",
		Note.items: "Itens da Nota",
	}

	column_searchable_list = [Note.note_number, Note.provider]
	column_filterable_list = [Note.note_type, Note.date_of_issue]


class ItemNoteAdmin(ModelView, model=ItemNote):
	name = "Itens da Nota"
	name_plural = "Itens das Notas"
	icon = "fa fa-boxes"
	category = "Financeiro"
	category_icon = "fa fa-dollar-sign"

	can_create = False
	can_edit = True
	can_delete = True
	can_view_details = True

	page_size = 50
	page_size_options = [25, 50, 100, 200]

	column_list = [
		ItemNote.id,
		ItemNote.note_id,
		ItemNote.product_name,
		ItemNote.product_code,
		ItemNote.quantity,
		ItemNote.unit_of_measure,
		ItemNote.unit_value,
		ItemNote.discount_value,
		ItemNote.icms_value,
		ItemNote.ipi_value,
		ItemNote.created_at,
	]

	column_labels = {
		ItemNote.id: "ID",
		ItemNote.note_id: "ID da Nota",
		ItemNote.product_name: "Nome do Produto",
		ItemNote.product_code: "Código do Produto",
		ItemNote.ncm: "NCM",
		ItemNote.cfop: "CFOP",
		ItemNote.quantity: "Quantidade",
		ItemNote.unit_of_measure: "Unidade",
		ItemNote.unit_value: "Valor Unitário",
		ItemNote.discount_value: "Desconto",
		ItemNote.icms_value: "ICMS",
		ItemNote.ipi_value: "IPI",
		ItemNote.created_at: "Criado em",
	}

	column_searchable_list = [ItemNote.product_name, ItemNote.product_code]
	column_filterable_list = [ItemNote.note_id, ItemNote.ncm, ItemNote.cfop]
