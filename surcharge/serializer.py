# -*- coding: utf-8 -*-


class MixinSerializer(object):

    """
    Serializer is use for retrieve the benchmark
    result in a specific format
    """

    def _default(self, res):
        """
        Returns the res in the raw format. (see: process.py)

        :param res: contains the results of a benchmark
        :type res: list[HttpRequest_namedtuple]
        """
        return res

    def _xml(self, res):
        """
        Returns the res in the XML format. (see: process.py)

        :param res: contains the results of a benchmark
        :type res: list[HttpRequest_namedtuple]
        """
        raise NotImplementedError('xml format')

    def _json(self, res):
        """
        Returns the res in the JSON format. (see: process.py)

        :param res: contains the results of a benchmark
        :type res: list[HttpRequest_namedtuple]
        """
        return [{'status_code': r.status_code, 'exec_time': r.exec_time} for r in res]
