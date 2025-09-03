"""
板块分析
"""


@api_blueprint.route('/sector_stocks', methods=['GET'])
@inject
def api_sector_stocks(capital_flow_analyzer: CapitalFlowAnalyzer = Provide[AnalysisContainer.capital_flow_analyzer]):
    try:
        sector = request.args.get('sector')
        if not sector:
            return {'error': 'Sector name is required'}, status.HTTP_400_BAD_REQUEST
        result = capital_flow_analyzer.get_sector_stocks(sector)
        return custom_jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error getting sector stocks: {e}", exc_info=True)
        return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
