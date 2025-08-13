# TODO: Figure out how tf to get opentelemetry integrated to begin with
# TODO: Figure out how to set up the app in the first place
# from opentelemetry import trace
#
#
# def add_open_telemetry_spans(_, __, event_dict):
#     span = trace.get_current_span()
#     if not span.is_recording():
#         event_dict["span"] = None
#         return event_dict
#
#     ctx = span.get_span_context()
#     parent = getattr(span, "parent", None)
#
#     event_dict["span"] = {
#         "span_id": format(ctx.span_id, "016x"),
#         "trace_id": format(ctx.trace_id, "032x"),
#         "parent_span_id": None
#         if not parent
#         else format(parent.span_id, "016x"),
#     }
#
#     return event_dict
