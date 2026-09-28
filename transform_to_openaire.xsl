<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:datacite="http://datacite.org/schema/kernel-4"
    xmlns:oaire="http://namespace.openaire.eu/schema/oaire/"
    exclude-result-prefixes="xsl oaire">

  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  <xsl:strip-space elements="*"/>

  <xsl:template match="/*">
			<resource
			  xmlns="http://namespace.openaire.eu/schema/oaire/"
			  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
			  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
			  xmlns:dc="http://purl.org/dc/elements/1.1/"
			  xmlns:dcterms="http://purl.org/dc/terms/"
			  xmlns:datacite="http://datacite.org/schema/kernel-4"
			  xsi:schemaLocation="http://namespace.openaire.eu/schema/oaire/ https://www.openaire.eu/schema/repo-lit/4.0/openaire.xsd">

			  <datacite:identifier identifierType="URL">
				  <xsl:choose>
					<xsl:when test="starts-with(identifier, 'ZA')">
					  <xsl:text>https://search.gesis.org/research_data/</xsl:text>
					  <xsl:value-of select="identifier"/>
					</xsl:when>
					<xsl:otherwise>
					  <xsl:text>https://search.gesis.org/publication/</xsl:text>
					  <xsl:value-of select="identifier"/>
					</xsl:otherwise>
				  </xsl:choose>
			  </datacite:identifier>
			  <xsl:if test="hasLink/*/hasIdentifier/item[usesIdentifierScheme='doi' and hasLiteralValue]
						  or hasLink/*/hasTarget[starts-with(., 'ZA')]
						  or hasLink/*/hasTarget[starts-with(., 'gesis-bib-')]">

				  <datacite:relatedIdentifiers>

					<!-- DOI from hasIdentifier -->
					<xsl:for-each select="hasLink/*/hasIdentifier/item[usesIdentifierScheme='doi' and hasLiteralValue]">
					  <datacite:relatedIdentifier relatedIdentifierType="DOI">
						<xsl:attribute name="relationType">
						  <xsl:choose>
							<xsl:when test="../../linkType='citation'">Cites</xsl:when>
							<xsl:when test="../../linkType='equivalent'">IsIdenticalTo</xsl:when>
							<xsl:otherwise>IsRelatedTo</xsl:otherwise>
						  </xsl:choose>
						</xsl:attribute>
						<xsl:value-of select="hasLiteralValue"/>
					  </datacite:relatedIdentifier>
					</xsl:for-each>

					<!-- URL from hasTarget = ZA... -->
					<xsl:for-each select="hasLink/*[hasTarget[starts-with(., 'ZA')]]">
					  <datacite:relatedIdentifier relatedIdentifierType="URL">
						<xsl:attribute name="relationType">
						  <xsl:choose>
							<xsl:when test="linkType='citation'">Cites</xsl:when>
							<xsl:when test="linkType='equivalent'">IsIdenticalTo</xsl:when>
							<xsl:otherwise>References</xsl:otherwise>
						  </xsl:choose>
						</xsl:attribute>
						<xsl:text>https://search.gesis.org/research_data/</xsl:text>
						<xsl:value-of select="hasTarget"/>
					  </datacite:relatedIdentifier>
					</xsl:for-each>

					<!-- URL from hasTarget = gesis-bib... -->
					<xsl:for-each select="hasLink/*[hasTarget[starts-with(., 'gesis-bib-')]]">
					  <datacite:relatedIdentifier relatedIdentifierType="URL">
						<xsl:attribute name="relationType">
						  <xsl:choose>
							<xsl:when test="linkType='citation'">Cites</xsl:when>
							<xsl:when test="linkType='equivalent'">IsIdenticalTo</xsl:when>
							<xsl:otherwise>References</xsl:otherwise>
						  </xsl:choose>
						</xsl:attribute>
						<xsl:text>https://search.gesis.org/publication/</xsl:text>
						<xsl:value-of select="hasTarget"/>
					  </datacite:relatedIdentifier>
					</xsl:for-each>

				  </datacite:relatedIdentifiers>

			  </xsl:if>

			  <datacite:creators>
				<xsl:for-each select="authors/*">
				  <datacite:creator>
					<datacite:creatorName>
					  <xsl:value-of select="name"/>
					</datacite:creatorName>
				  </datacite:creator>
				</xsl:for-each>
			  </datacite:creators>

			  <datacite:titles>
				<datacite:title>
				  <xsl:value-of select="title"/>
				</datacite:title>
			  </datacite:titles>
			  
			  <dc:publisher>
				  <xsl:choose>
					<xsl:when test="publisher/*/name">
					  <xsl:value-of select="publisher/*/name"/>
					</xsl:when>
					<xsl:otherwise>GESIS</xsl:otherwise>
				  </xsl:choose>
			  </dc:publisher>

			  <datacite:dates>
				  <datacite:date dateType="Issued">
					<xsl:choose>
					  <xsl:when test="date_pub">
						<xsl:value-of select="date_pub"/>
					  </xsl:when>
					  <xsl:otherwise>0000</xsl:otherwise>
					</xsl:choose>
				  </datacite:date>
			  </datacite:dates>

			  <xsl:if test="topics/*/name">
				<datacite:subjects>
				  <xsl:for-each select="topics/*">
					<datacite:subject>
					  <xsl:value-of select="name"/>
					</datacite:subject>
				  </xsl:for-each>
				</datacite:subjects>
			  </xsl:if>

			  <xsl:if test="contributors/*/name">
				<datacite:contributors>
				  <xsl:for-each select="contributors/*">
					<datacite:contributor>
					  <datacite:contributorName>
						<xsl:value-of select="name"/>
					  </datacite:contributorName>
					</datacite:contributor>
				  </xsl:for-each>
				</datacite:contributors>
			  </xsl:if>

			  <xsl:if test="language/item">
				<dc:language>
				  <xsl:value-of select="language/item[1]"/>
				</dc:language>
			  </xsl:if>

			  <xsl:if test="doctype/en">
				<resourceType resourceTypeGeneral="Publication" xml:lang="en">
				  <xsl:value-of select="doctype/en"/>
				</resourceType>
			  </xsl:if>
			  
			  <resourceType resourceTypeGeneral="literature">
			  <xsl:attribute name="uri">
						  <xsl:choose>
							<xsl:when test="doctype/en='book'">http://purl.org/coar/resource_type/c_2f33</xsl:when>
							<xsl:when test="doctype/en='journal_article'">http://purl.org/coar/resource_type/c_6501</xsl:when>
							<xsl:otherwise>http://purl.org/coar/resource_type/c_1843</xsl:otherwise>
						  </xsl:choose>
						</xsl:attribute>
						<xsl:choose>
							<xsl:when test="doctype/en='book'">book</xsl:when>
							<xsl:when test="doctype/en='journal_article'">journal article</xsl:when>
							<xsl:otherwise>other</xsl:otherwise>
						  </xsl:choose>
			  </resourceType>
			  
				  <licenseCondition>
					<xsl:value-of select="metadataLicense"/>
				  </licenseCondition> 
				  
				  <datacite:rights rightsURI="http://purl.org/coar/access_right/c_14cb">metadata only access</datacite:rights>

			  
			  <xsl:if test="src_journal/*/name">
				  <dc:source>
					<xsl:value-of select="src_journal/*/name"/>
				  </dc:source>
			  </xsl:if>

		<!--	  <version>0.2</version> -->

<!--			  <xsl:if test="library_location/*/name">
				<datacite:geoLocations>
				  <xsl:for-each select="library_location/*">
					<datacite:geoLocation>
					  <datacite:geoLocationPlace>
						<xsl:value-of select="name"/>
					  </datacite:geoLocationPlace>
					</datacite:geoLocation>
				  </xsl:for-each>
				</datacite:geoLocations>
			  </xsl:if> -->

			</resource>

  </xsl:template>

</xsl:stylesheet>