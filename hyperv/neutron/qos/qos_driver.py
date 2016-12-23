from oslo_log import log as logging

from neutron.agent.l2.extensions import qos
from os_win.utils.network import networkutils

LOG = logging.getLogger(__name__)


class QosHyperVAgentDriver(qos.QosAgentDriver):

    def __init__(self):
        super(QosHyperVAgentDriver, self).__init__()

    def initialize(self):
        LOG.debug("QosHyperVAgentDriver -initialize-")
        self.utils = networkutils.NetworkUtils()

    def consume_api(self, agent_api):
        LOG.debug("QosHyperVAgentDriver -consume_api-")

    def create(self, port, qos_policy):
        """Apply QoS rules on port for the first time.

        :param port: port object.
        :param qos_policy: the QoS policy to be applied on port.
        """
        LOG.debug("QosHyperVAgentDriver -create-")
        policy_data = self._get_policy_values(qos_policy)
        self.utils.set_qos_rule_on_port(port["port_id"], policy_data)

    def update(self, port, qos_policy):
        """Apply QoS rules on port.

        :param port: port object.
        :param qos_policy: the QoS policy to be applied on port.
        """
        LOG.debug("QosHyperVAgentDriver -update-")
        policy_data = self._get_policy_values(qos_policy)
        self.utils.set_qos_rule_on_port(port["port_id"], policy_data)

    def delete(self, port, qos_policy=None):
        """Remove QoS rules from port.

        :param port: port object.
        :param qos_policy: the QoS policy to be removed from port.
        """
        LOG.debug("QosHyperVAgentDriver -delete-")
        self.utils.remove_qos_rule_from_port(port["port_id"])

    def _get_policy_values(self, qos_policy):
        LOG.debug("Getting policy values")

        qos_rules = qos_policy.rules
        qos_min = None
        qos_max = None
        for qos_rule in qos_rules:
            LOG.debug("qos rule: %s" % qos_rule)
            if hasattr(qos_rule, "min_kbps"):
                qos_min = getattr(qos_rule, "min_kbps")
            if hasattr(qos_rule, "max_kbps"):
                qos_max = getattr(qos_rule, "max_kbps")

        result = {
            "min_kbps": qos_min,
            "max_kbps": qos_max
        }

        return result
