import unittest
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from server import app


class GeneralTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_redirect_root_to_docs(self):
        response = self.client.get("/")

        self.assertEqual(response.url, "http://testserver/docs")

    @patch("database.SessionLocal")
    def test_get_db(self, mock_session_local):
        mock_session = Mock(spec=Session)

        mock_session_local.return_value = mock_session

        db_generator = get_db()
        db = next(db_generator)

        self.assertEqual(db, mock_session)


class EmpresaRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        TestingSessionLocal = sessionmaker(self.engine, autoflush=False, expire_on_commit=False)

        Base.metadata.create_all(self.engine)

        def override_get_db():
            db = TestingSessionLocal()

            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db

        self.client = TestClient(app)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_create_empresa(self):
        response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.json()

        self.assertEqual(data["nome"], "Empresa Teste")
        self.assertEqual(data["cnpj"], "12345678901234")

    def test_create_empresa_duplicada(self):
        self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        self.assertEqual(response.status_code, 400)

        data = response.json()

        self.assertEqual(data["message"], "Empresa já cadastrada")

    def test_read_empresas(self):
        self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )
        self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste 2",
                "cnpj": "56789012345678",
                "endereco": "Rua Teste 2",
                "email": "teste2@email.com",
                "telefone": "23456789012",
            },
        )

        response = self.client.get("/empresas/")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 2)

    def test_read_empresa(self):
        response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.json()

        empresa_id = data["id"]

        response = self.client.get(f"/empresas/{empresa_id}")

        data = response.json()

        self.assertEqual(data["nome"], "Empresa Teste")

    def test_read_empresa_empresa_nao_encontrada(self):
        response = self.client.get("/empresas/1")

        self.assertEqual(response.status_code, 404)

    def test_update_empresa(self):
        response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        data = response.json()

        empresa_id = data["id"]

        response = self.client.put(
            f"/empresas/{empresa_id}",
            json={
                "nome": "Empresa Atualizada",
                "endereco": "Rua Atualizada",
                "email": "testeA@email.com",
                "telefone": "23456789012",
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["nome"], "Empresa Atualizada")
        self.assertEqual(data["cnpj"], "12345678901234")

    def test_update_empresa_empresa_nao_encontrada(self):
        self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        response = self.client.put(
            "/empresas/2",
            json={
                "nome": "Empresa Atualizada",
                "endereco": "Rua Atualizada",
                "email": "testeA@email.com",
                "telefone": "23456789012",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_empresa(self):
        response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        data = response.json()

        empresa_id = data["id"]

        response = self.client.delete(f"/empresas/{empresa_id}")

        self.assertEqual(response.status_code, 204)

    def test_delete_empresa_empresa_nao_encontrada(self):
        self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        response = self.client.delete("/empresas/2")

        self.assertEqual(response.status_code, 404)


class ObrigacaoAcessoriaRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        TestingSessionLocal = sessionmaker(self.engine, autoflush=False, expire_on_commit=False)

        Base.metadata.create_all(self.engine)

        def override_get_db():
            db = TestingSessionLocal()

            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db

        self.client = TestClient(app)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_create_obrigacao(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        response = self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": empresa_id,
            },
        )

        self.assertEqual(response.status_code, 201)

        data = response.json()

        self.assertEqual(data["nome"], "Obrigação Teste")
        self.assertEqual(data["periodicidade"], "mensal")

    def test_create_obrigacao_empresa_id_invalido(self):
        response = self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": 1,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_create_obrigacao_periodicidade_invalida(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        response = self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "semanal",
                "empresa_id": empresa_id,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_read_obrigacoes(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": empresa_id,
            },
        )
        self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste 2",
                "periodicidade": "trimestral",
                "empresa_id": empresa_id,
            },
        )

        response = self.client.get("/obrigacoes/")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 2)

    def test_read_obrigacao(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        response = self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": empresa_id,
            },
        )

        data = response.json()

        obrigacao_id = data["id"]

        response = self.client.get(f"/obrigacoes/{obrigacao_id}")

        self.assertEqual(response.status_code, 200)

    def test_read_obrigacao_obrigacao_nao_encontrada(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": empresa_id,
            },
        )

        response = self.client.get("/obrigacoes/2")

        self.assertEqual(response.status_code, 404)

    def test_update_obrigacao(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        response = self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": empresa_id,
            },
        )

        data = response.json()

        obrigacao_id = data["id"]

        response = self.client.put(
            f"/obrigacoes/{obrigacao_id}",
            json={
                "nome": "Obrigação Teste Atualizada",
                "periodicidade": "anual",
                "empresa_id": empresa_id,
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["nome"], "Obrigação Teste Atualizada")
        self.assertEqual(data["periodicidade"], "anual")

    def test_update_obrigacao_periodicidade_invalida(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        response = self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": empresa_id,
            },
        )

        data = response.json()

        obrigacao_id = data["id"]

        response = self.client.put(
            f"/obrigacoes/{obrigacao_id}",
            json={
                "nome": "Obrigação Teste Atualizada",
                "periodicidade": "semanal",
                "empresa_id": empresa_id,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_update_obrigacao_obrigacao_nao_encontrada(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": empresa_id,
            },
        )

        response = self.client.put(
            "/obrigacoes/2",
            json={
                "nome": "Obrigação Teste Atualizada",
                "periodicidade": "anual",
                "empresa_id": empresa_id,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_update_obrigacao_empresa_id_invalido(self):
        self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        response = self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": 1,
            },
        )

        data = response.json()

        obrigacao_id = data["id"]

        response = self.client.put(
            f"/obrigacoes/{obrigacao_id}",
            json={
                "nome": "Obrigação Teste Atualizada",
                "periodicidade": "anual",
                "empresa_id": 2,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_obrigacao(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        response = self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": empresa_id,
            },
        )

        data = response.json()

        obrigacao_id = data["id"]

        response = self.client.delete(f"/obrigacoes/{obrigacao_id}")

        self.assertEqual(response.status_code, 204)

    def test_delete_obrigacao_obrigacao_nao_encontrada(self):
        empresa_response = self.client.post(
            "/empresas/",
            json={
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste",
                "email": "teste@email.com",
                "telefone": "12345678901",
            },
        )

        empresa_data = empresa_response.json()
        empresa_id = empresa_data["id"]

        self.client.post(
            "/obrigacoes/",
            json={
                "nome": "Obrigação Teste",
                "periodicidade": "mensal",
                "empresa_id": empresa_id,
            },
        )

        response = self.client.delete("/obrigacoes/2")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
