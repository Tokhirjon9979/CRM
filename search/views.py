# import abc
#
# from django.http import HttpResponse
# from elasticsearch_dsl import Q
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.views import APIView
#
# from company.documents import UserDocument, CompanyDocument
# from company.serializers import UserSerializer, CompanyySerializer
#
#
# class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
#     serializer_class = None
#     document_class = None
#
#     @abc.abstractmethod
#     def generate_q_expression(self, query):
#         """This method should be overridden
#         and return a Q() expression."""
#
#     def get(self, request, query):
#         try:
#             q = self.generate_q_expression(query)
#             search = self.document_class.search().query(q)
#             response = search.execute()
#
#             print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')
#
#             results = self.paginate_queryset(response, request, view=self)
#             print(1)
#             serializer = self.serializer_class(results, many=True)
#             print(results)
#             print(serializer.data)
#             return self.get_paginated_response(serializer.data)
#         except Exception as e:
#             print(3)
#             return HttpResponse(e, status=500)
#
#
# # views
#
#
# class SearchUsers(PaginatedElasticSearchAPIView):
#     serializer_class = UserSerializer
#     document_class = UserDocument
#
#     def generate_q_expression(self, query):
#         return Q('bool',
#                  should=[
#                      Q('match', username=query),
#                      Q('match', first_name=query),
#                      Q('match', last_name=query),
#                  ], minimum_should_match=1)
#
#
# class SearchCompanies(PaginatedElasticSearchAPIView):
#     serializer_class = CompanyySerializer
#     document_class = CompanyDocument
#
#     def generate_q_expression(self, query):
#         return Q(
#             'multi_match', query=query,
#             fields=[
#                 'name',
#             ], fuzziness='auto')
