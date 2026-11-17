<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:oai="http://schema.datacite.org/oai/oai-1.1/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    exclude-result-prefixes="xsl">

  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  <xsl:strip-space elements="*"/>

  <xsl:template match="/*">
    
	<xsl:if test="hasIdentifier/item[usesIdentifierScheme='doi']/hasLiteralValue">
				  
		<oai_datacite
		  xmlns="http://schema.datacite.org/oai/oai-1.1/"
		  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
		  xsi:schemaLocation="http://schema.datacite.org/oai/oai-1.1/ http://schema.datacite.org/oai/oai-1.1/oai.xsd">

		  <isReferenceQuality>true</isReferenceQuality>
		  <schemaVersion>4</schemaVersion>
		  <datacentreSymbol>GESIS</datacentreSymbol>

		  <payload>
			<resource
			  xmlns="http://datacite.org/schema/kernel-4"
			  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
			  xsi:schemaLocation="http://datacite.org/schema/kernel-4 https://schema.datacite.org/meta/kernel-4/metadata.xsd">

			  <identifier identifierType="DOI">
				  <xsl:value-of select="hasIdentifier/item[usesIdentifierScheme='doi']/hasLiteralValue[1]"/>
			 </identifier>
			  <xsl:if test="hasLink/*/hasIdentifier/item[usesIdentifierScheme='doi' and hasLiteralValue]">

				  <relatedIdentifiers>

					<!-- DOI from hasIdentifier -->
					<xsl:for-each select="hasLink/*/hasIdentifier/item[usesIdentifierScheme='doi' and hasLiteralValue]">
					  <relatedIdentifier relatedIdentifierType="DOI">
						<xsl:attribute name="relationType">
						  <xsl:choose>
							<xsl:when test="../../linkType='citation'">References</xsl:when>
							<xsl:when test="../../linkType='equivalent'">IsIdenticalTo</xsl:when>
							<xsl:otherwise>IsRelatedTo</xsl:otherwise>
						  </xsl:choose>
						</xsl:attribute>
						<xsl:value-of select="hasLiteralValue"/>
					  </relatedIdentifier>
					</xsl:for-each>

				  </relatedIdentifiers>

			  </xsl:if>

			  <creators>
				<xsl:for-each select="authors/*">
				  <creator>
					<creatorName>
					  <xsl:value-of select="name"/>
					</creatorName>
				  </creator>
				</xsl:for-each>
			  </creators>

			  <titles>
				<title>
				  <xsl:value-of select="title"/>
				</title>
			  </titles>
			  
			  <publisher>
				  <xsl:choose>
					<xsl:when test="publisher/*/name">
					  <xsl:value-of select="publisher/*/name"/>
					</xsl:when>
					<xsl:otherwise>GESIS</xsl:otherwise>
				  </xsl:choose>
			  </publisher>
			  
			  <publicationYear>
				  <xsl:choose>
					<xsl:when test="date_pub">
					  <xsl:value-of select="date_pub"/>
					</xsl:when>
					<xsl:otherwise>0000</xsl:otherwise>
				  </xsl:choose>
			  </publicationYear>

			  <dates>
				  <date dateType="Issued">
					<xsl:choose>
					  <xsl:when test="date_pub">
						<xsl:value-of select="date_pub"/>
					  </xsl:when>
					  <xsl:otherwise>0000</xsl:otherwise>
					</xsl:choose>
				  </date>
			  </dates>

			  <xsl:if test="topics/*/name">
				<subjects>
				  <xsl:for-each select="topics/*">
					<subject>
					  <xsl:value-of select="name"/>
					</subject>
				  </xsl:for-each>
				</subjects>
			  </xsl:if>

			  <xsl:if test="contributors/*/name">
				<contributors>
				  <xsl:for-each select="contributors/*">
					<contributor>
					  <contributorName>
						<xsl:value-of select="name"/>
					  </contributorName>
					</contributor>
				  </xsl:for-each>
				</contributors>
			  </xsl:if>

			  <xsl:if test="language/item">
				<language>
				  <xsl:value-of select="language/item[1]"/>
				</language>
			  </xsl:if>

			  <xsl:if test="doctype/en">
				<resourceType xml:lang="en">
				  <xsl:value-of select="doctype/en"/>
				</resourceType>
			  </xsl:if>
			  
			  <rightsList>
				  <rights>
					<xsl:value-of select="metadataLicense"/>
				  </rights>
			  </rightsList>
			  
			  <xsl:if test="src_journal/*/name">
				  <source>
					<xsl:value-of select="src_journal/*/name"/>
				  </source>
			  </xsl:if>

			  <version>0.2</version>

			  <xsl:if test="library_location/*/name">
				<geoLocations>
				  <xsl:for-each select="library_location/*">
					<geoLocation>
					  <geoLocationPlace>
						<xsl:value-of select="name"/>
					  </geoLocationPlace>
					</geoLocation>
				  </xsl:for-each>
				</geoLocations>
			  </xsl:if>

			</resource>
		  </payload>
		</oai_datacite>
	</xsl:if>
  </xsl:template>

</xsl:stylesheet>