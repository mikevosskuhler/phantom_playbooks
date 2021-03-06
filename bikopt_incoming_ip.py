"""
test playbook
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'geolocate_ip_1' block
    geolocate_ip_1(container=container)

    # call 'whois_ip_1' block
    whois_ip_1(container=container)

    # call 'lookup_ip_1' block
    lookup_ip_1(container=container)

    return

def geolocate_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('geolocate_ip_1() called')

    # collect data for 'geolocate_ip_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'geolocate_ip_1' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'ip': container_item[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    phantom.act("geolocate ip", parameters=parameters, assets=['maxmind'], callback=join_format_1, name="geolocate_ip_1")

    return

def whois_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('whois_ip_1() called')

    # collect data for 'whois_ip_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'whois_ip_1' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'ip': container_item[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    phantom.act("whois ip", parameters=parameters, assets=['whois'], callback=join_format_1, name="whois_ip_1")

    return

def lookup_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('lookup_ip_1() called')

    # collect data for 'lookup_ip_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'lookup_ip_1' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'ip': container_item[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    phantom.act("lookup ip", parameters=parameters, assets=['google_dns'], callback=join_format_1, name="lookup_ip_1")

    return

def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('format_1() called')
    
    template = """ipaddress={0}, continent={1}, country={2}, lat={3}, lon={4},postal_code={5},asn={6},summary={8},message={7}"""

    # parameter list for template variable replacement
    parameters = [
        "artifact:*.cef.sourceAddress",
        "geolocate_ip_1:action_result.data.*.continent_name",
        "geolocate_ip_1:action_result.data.*.country_name",
        "geolocate_ip_1:action_result.data.*.latitude",
        "geolocate_ip_1:action_result.data.*.longitude",
        "geolocate_ip_1:action_result.data.*.postal_code",
        "whois_ip_1:action_result.data.*.asn",
        "lookup_ip_1:action_result.summary.hostname",
        "lookup_ip_1:action_result.message",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_1")

    post_data_1(container=container)

    return

def join_format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('join_format_1() called')

    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'geolocate_ip_1', 'whois_ip_1', 'lookup_ip_1' ]):
        
        # call connected block "format_1"
        format_1(container=container, handle=handle)
    
    return

def post_data_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('post_data_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'post_data_1' call
    formatted_data_1 = phantom.get_format_data(name='format_1')

    parameters = []
    
    # build parameters list for 'post_data_1' call
    parameters.append({
        'index': "phantom",
        'host': "local phantom",
        'data': formatted_data_1,
        'source': "Phantom_events",
        'source_type': "Automation/Orchestration Platform",
    })

    phantom.act("post data", parameters=parameters, assets=['local splunk'], name="post_data_1")

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions 
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return