"""
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'run_query_2' block
    run_query_2(container=container)

    return

def run_query_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('run_query_2() called')

    # collect data for 'run_query_2' call

    parameters = []
    
    # build parameters list for 'run_query_2' call
    parameters.append({
        'query': "index=_internal sourcetype=splunkd_ui_access  | head 10",
        'display': "",
    })

    phantom.act("run query", parameters=parameters, assets=['local splunk'], name="run_query_2")

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