from typing import Dict, List, Tuple
from models.stock import Stock
from models.recommendation import RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, MIN_SCORE, MAX_SCORE,
    SR_LOOKBACK_PERIOD, SR_SUPPORT_TOLERANCE, SR_RESISTANCE_TOLERANCE, SR_MIN_TOUCHES,
    SR_MIN_DATA_LENGTH, SR_CONFIDENCE, SR_CONFIDENCE_INSUFFICIENT_DATA,
    SR_CONFIDENCE_NO_LEVELS, SR_CONFIDENCE_ERROR,
    SR_DISTANCE_VERY_CLOSE, SR_DISTANCE_CLOSE, SR_DISTANCE_NEAR,
    SR_SCORE_NEAR_SUPPORT_VERY_CLOSE, SR_SCORE_NEAR_SUPPORT_CLOSE,
    SR_SCORE_NEAR_RESISTANCE_VERY_CLOSE, SR_SCORE_NEAR_RESISTANCE_CLOSE,
    SR_SCORE_NEAR_SUPPORT_NEAR, SR_SCORE_NEAR_RESISTANCE_NEAR,
    SR_RISK_REWARD_FAVORABLE, SR_RISK_REWARD_POOR,
    SR_SCORE_FAVORABLE_RR, SR_SCORE_POOR_RR
)
import yfinance as yf
import numpy as np

class SupportResistanceAnalyzer(BaseAnalyzer):
    """Analyzer based on support and resistance levels from historical price data"""
    
    def __init__(self, weight: float = 1.0):
        super().__init__("Support/Resistance Analysis", weight)
        self.lookback_period = SR_LOOKBACK_PERIOD
        self.support_tolerance = SR_SUPPORT_TOLERANCE
        self.resistance_tolerance = SR_RESISTANCE_TOLERANCE
        self.min_touches = SR_MIN_TOUCHES
    
    def find_support_resistance_levels(self, prices: List[float]) -> Tuple[List[float], List[float]]:
        """Identify support and resistance levels from price history"""
        if len(prices) < SR_MIN_DATA_LENGTH:
            return [], []
        
        support_levels = []
        resistance_levels = []
        
        # Find local minima (potential support) and maxima (potential resistance)
        for i in range(1, len(prices) - 1):
            # Local minimum (support)
            if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
                support_levels.append(prices[i])
            # Local maximum (resistance)
            elif prices[i] > prices[i-1] and prices[i] > prices[i+1]:
                resistance_levels.append(prices[i])
        
        # Cluster similar levels together
        def cluster_levels(levels: List[float], tolerance: float) -> List[float]:
            if not levels:
                return []
            
            levels = sorted(levels)
            clusters = []
            current_cluster = [levels[0]]
            
            for level in levels[1:]:
                # Check if level is within tolerance of current cluster
                cluster_avg = sum(current_cluster) / len(current_cluster)
                if abs(level - cluster_avg) / cluster_avg <= tolerance:
                    current_cluster.append(level)
                else:
                    # Save current cluster if it has enough touches
                    if len(current_cluster) >= self.min_touches:
                        clusters.append(sum(current_cluster) / len(current_cluster))
                    current_cluster = [level]
            
            # Add last cluster
            if len(current_cluster) >= self.min_touches:
                clusters.append(sum(current_cluster) / len(current_cluster))
            
            return clusters
        
        support_clusters = cluster_levels(support_levels, self.support_tolerance)
        resistance_clusters = cluster_levels(resistance_levels, self.resistance_tolerance)
        
        return support_clusters, resistance_clusters
    
    def analyze(self, stock: Stock) -> Dict:
        """Analyze stock based on support and resistance levels"""
        score = DEFAULT_SCORE  # Start neutral
        reasons = []
        confidence = SR_CONFIDENCE
        
        try:
            ticker = yf.Ticker(stock.symbol)
            hist = ticker.history(period=self.lookback_period)
            
            if hist.empty or len(hist) < SR_MIN_DATA_LENGTH:
                reasons.append("Insufficient historical data for S/R analysis")
                confidence = SR_CONFIDENCE_INSUFFICIENT_DATA
            else:
                prices = hist['Close'].tolist()
                current_price = stock.current_price
                
                # Find support and resistance levels
                support_levels, resistance_levels = self.find_support_resistance_levels(prices)
                
                # Sort levels
                support_levels = sorted(support_levels, reverse=True)  # Highest first
                resistance_levels = sorted(resistance_levels)  # Lowest first
                
                # Find nearest support and resistance
                nearest_support = None
                nearest_resistance = None
                
                for support in support_levels:
                    if support < current_price:
                        nearest_support = support
                        break
                
                for resistance in resistance_levels:
                    if resistance > current_price:
                        nearest_resistance = resistance
                        break
                
                # Analyze position relative to S/R levels
                if nearest_support and nearest_resistance:
                    support_distance = ((current_price - nearest_support) / nearest_support) * 100
                    resistance_distance = ((nearest_resistance - current_price) / current_price) * 100
                    
                    # Score based on position
                    if support_distance < SR_DISTANCE_VERY_CLOSE:
                        score += SR_SCORE_NEAR_SUPPORT_VERY_CLOSE
                        reasons.append(
                            f"Near strong support at ${nearest_support:.2f} "
                            f"({support_distance:.2f}% away) - potential bounce"
                        )
                    elif support_distance < SR_DISTANCE_CLOSE:
                        score += SR_SCORE_NEAR_SUPPORT_CLOSE
                        reasons.append(
                            f"Approaching support at ${nearest_support:.2f} "
                            f"({support_distance:.2f}% away)"
                        )
                    
                    if resistance_distance < SR_DISTANCE_VERY_CLOSE:
                        score += SR_SCORE_NEAR_RESISTANCE_VERY_CLOSE
                        reasons.append(
                            f"Near strong resistance at ${nearest_resistance:.2f} "
                            f"({resistance_distance:.2f}% away) - potential rejection"
                        )
                    elif resistance_distance < SR_DISTANCE_CLOSE:
                        score += SR_SCORE_NEAR_RESISTANCE_CLOSE
                        reasons.append(
                            f"Approaching resistance at ${nearest_resistance:.2f} "
                            f"({resistance_distance:.2f}% away)"
                        )
                    
                    # Risk/reward ratio
                    if nearest_support and nearest_resistance:
                        risk = current_price - nearest_support
                        reward = nearest_resistance - current_price
                        if risk > 0:
                            risk_reward_ratio = reward / risk
                            if risk_reward_ratio > SR_RISK_REWARD_FAVORABLE:
                                score += SR_SCORE_FAVORABLE_RR
                                reasons.append(f"Favorable risk/reward ratio ({risk_reward_ratio:.2f}:1)")
                            elif risk_reward_ratio < SR_RISK_REWARD_POOR:
                                score += SR_SCORE_POOR_RR
                                reasons.append(f"Poor risk/reward ratio ({risk_reward_ratio:.2f}:1)")
                    
                    # Add level information
                    reasons.insert(0, 
                        f"Support: ${nearest_support:.2f} | "
                        f"Resistance: ${nearest_resistance:.2f} | "
                        f"Current: ${current_price:.2f}"
                    )
                
                elif nearest_support:
                    support_distance = ((current_price - nearest_support) / nearest_support) * 100
                    if support_distance < SR_DISTANCE_NEAR:
                        score += SR_SCORE_NEAR_SUPPORT_NEAR
                        reasons.append(f"Near support at ${nearest_support:.2f} - potential bounce")
                    reasons.insert(0, f"Support: ${nearest_support:.2f} | Current: ${current_price:.2f}")
                
                elif nearest_resistance:
                    resistance_distance = ((nearest_resistance - current_price) / current_price) * 100
                    if resistance_distance < SR_DISTANCE_NEAR:
                        score += SR_SCORE_NEAR_RESISTANCE_NEAR
                        reasons.append(f"Near resistance at ${nearest_resistance:.2f} - potential rejection")
                    reasons.insert(0, f"Resistance: ${nearest_resistance:.2f} | Current: ${current_price:.2f}")
                
                else:
                    reasons.append("No clear support/resistance levels identified")
                    confidence = SR_CONFIDENCE_NO_LEVELS
        
        except Exception as e:
            reasons.append(f"Error in S/R analysis: {str(e)}")
            confidence = SR_CONFIDENCE_ERROR
        
        # Normalize score
        score = max(MIN_SCORE, min(MAX_SCORE, score))
        
        recommendation_type = self.calculate_recommendation_type(score)
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons) if reasons else "No S/R indicators",
            'confidence': confidence,
            'recommendation_type': recommendation_type
        }

